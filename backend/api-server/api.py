import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")) + "\\yt-downloader")
from fastapi import FastAPI
from downloader import downloadVideo

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# test
@app.get("/")
def download(url: str, type: str, outputPath=None):
    name, path = downloadVideo(url, type, outputPath)

    return {f"Video downloaded successfully / Name: {name} / Path: {path}"}