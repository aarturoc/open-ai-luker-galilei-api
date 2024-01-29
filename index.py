from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Form
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
openai.api_key = config('OPENAI_API_KEY')

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
    print("file: " + RespFromWhisper +" question: "+question)
    if question == "¿Quién es la dueña de la gata?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Qué le gusta hacer a la gata?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Por qué está preocupada María?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿De donde salían los maullidos?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Por qué crees que eran suabes los maullidos?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Cuántos gatitos tuvo la gata María?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Qué le dijo la mama a María?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Para donde se fue maría tan apurada?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "¿Qué noticias le va a dar María a Lorena?:":
        ValidationFromChat = RequestFromText(question, RespFromWhisper)
    if question == "":
        ValidationFromChat = "Error, there is no question in the value"
    
    
    return ValidationFromChat

@app.post("/file/upload3")
async def uploadfile(file:UploadFile = File(...)):
    Response = await upload(file)
    RespFromWhisper = Response["transcript"]
    
    response = CompareFromText(re.sub(r'[^a-zA-Z0-9áéíóúü ]', '', RespFromWhisper).lower())

    return response