import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")) + "\\yt-downloader")
from fastapi import FastAPI
from downloader import downloadVideo

app = FastAPI()

@app.get("/")
def download(url: str, type: str, outputPath=None):
    name, path = downloadVideo(url, type, outputPath)

    return {f"Video downloaded successfully / Name: {name} / Path: {path}"}