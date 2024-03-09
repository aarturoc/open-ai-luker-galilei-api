from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from secrets import token_hex
from decouple import config
import uvicorn
import re
import openai
import json
import os
from openai import OpenAI
from FolderUploadFiel.UploadFiel import upload
from galilei_egra.egra.comprension import RequestFromText
from galilei_egra.egra.conversation import CompareFromText

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Conetion with Open Ai 
openai.api_key = config('OPENAI_API_KEY')
#Connection with mongo
client = MongoClient(config('MONGO_URL'))
db = client.get_database()
collection = db["InfoAudio"]

@app.get("/health-check")
def read_root():
    return{"Status Code":"200 OK"}

@app.post("/file/upload")
async def uploadfile(file:UploadFile = File(...)):
    Response = await upload(file)
    return Response

@app.post("/file/upload2")
async def uploadfile(file:UploadFile = File(...), question: Optional[str] = Form(None)):
    Response = await upload(file)
    RespFromWhisper = Response["transcript"]
     
    if question == "":
        ValidationFromChat = "Error, there is no question in the value"
    else:
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    
    
    return ValidationFromChat

@app.post("/file/upload3")
async def uploadfile(file:UploadFile = File(...)):
    Response = await upload(file)
    RespFromWhisper = Response["transcript"]
    
    response = CompareFromText(re.sub(r'[^a-zA-Z0-9áéíóúü ]', '', RespFromWhisper).lower())

    return response

@app.post("/MongoDB/AddAudio")
async def uploadfile(id: Optional[str] = Form(None), description: Optional[str] = Form(None), file:UploadFile = File(...)):
    try:
        content = await file.read()

        audio_data = {"id":id, "description":description,"name":file.filename,"AudioFile":content}
        result = collection.insert_one(audio_data)

        if result.inserted_id:
            return JSONResponse(content={"message":"Audio File and Information upload successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Error while uploading the audio file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.get("/MongoDB/GetAudio/{id}")
async def getAudio(id: str):
    try:
        projection = {"id":id,"description":1,"name":1,"AudioFile":1}
        audio_document = collection.find_one({"id":id}, projection)

        if audio_document:
            audio_document["_id"] = str(audio_document["_id"])
            content = audio_document["AudioFile"]
            name = audio_document["name"]
            return StreamingResponse(iter([content]),media_type="audio/mp3", headers={"Content-Disposition":f'attachment; name="{name}"'})
        else:
            raise HTTPException(status_code=404, detail="Audio fil not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.get("/MongoDB/GetInfoAudio/{id}")
async def getInfoAudio(id: str):
    try:
        projection = {"id":id,"description":1,"name":1}
        audio_document = collection.find_one({"id":id}, projection)

        if audio_document:
            audio_document["_id"] = str(audio_document["_id"])
            return JSONResponse(content={"message":"Audio information","data":audio_document},status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Audio fil not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

@app.get("/MongoDB/GetInfoAudio/")
async def getInfoAudio():
    # Fetch data from MongoDB
    data = list(collection.find())
    data["_id"] = int(data["_id"])
    return [list(collection.find(document)) for document in data]