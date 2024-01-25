from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form
from secrets import token_hex
from decouple import config
import uvicorn
import openai
import json
import os
from openai import OpenAI
from FolderUploadFiel.UploadFiel import upload
from galilei_egra.egra.comprension import RequestFromText

app = FastAPI()
openai.api_key = config('OPENAI_API_KEY')

@app.get("/")
def read_root():
    return{"Hello":"FastAPI"}

@app.post("/file/upload")
async def uploadfile(file:UploadFile = File(...)):
    Response = await upload(file)
    return Response

@app.post("/file/upload2")
async def uploadfile(file:UploadFile = File(...), question: Optional[str] = Form(None)):
    Response = await upload(file)
    RespFromWhisper = Response["transcript"]
    ValidationFromChat = RequestFromText(question, RespFromWhisper)
    
    return ValidationFromChat