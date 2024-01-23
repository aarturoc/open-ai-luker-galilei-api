from fastapi import FastAPI, UploadFile, File
from secrets import token_hex
from decouple import config
import uvicorn
import openai
import json
import os
from openai import OpenAI


app = FastAPI()
openai.api_key = config('OPENAI_API_KEY')

@app.get("/")
def read_root():
    return{"Hello":"FastAPI"}

@app.post("/file/upload")
async def upload(file:UploadFile = File(...)):
    file_ext = file.filename.split(".").pop()
    #file_name = token_hex(10)
    file_name = file.filename
    #file_path = f"{file_name}.{file_ext}"
    file_path = file_name
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)


        # Open the audio file
        audio_file_path = file_path
        audio_file = open(audio_file_path, "rb")

        # Make the transcription request
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file= audio_file,
            response_format="text",
            language="es",
        )
        transcript = transcription

        # Imprime la transcripción
        print("Transcripción:")
        print(transcript)

        # Cierra el archivo de audio
        audio_file.close()

    os.remove(file_path)

    return {"success":True, "file_path":file_path, "message":"File upload succesfully", "transcript": transcript}