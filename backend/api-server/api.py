import os, sys
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware


current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, '../yt-downloader'))
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
def hello_world():
    return {"message": "Hello World"}

# download in the backend
@app.post("/download")
def download(url: str, type: str):
    # 以固定的path去實作 
    name, path = downloadVideo(url, type, "./videos/")
    
    return {"message": "Video downloaded successfully",
            "name":{name}
            }
 
# upload to user 
@app.post("/video/{video_id}")
async def read_item(video_id: str):
    headers = {}
    video_content = None
    if video_id.endswith(".mp4"):
        headers["Content-Type"] = "video/mp4"
        headers["Content-Disposition"] = "attachment; filename=video.mp4"
        with open(f"./videos/{video_id}", "rb") as video_file:
            video_content = video_file.read()
        return Response(content=video_content, headers=headers)
    elif video_id.endswith(".wmv"):
        headers["Content-Type"] = "video/x-ms-wmv"
        headers["Content-Disposition"] = "attachment; filename=video.wmv"
        with open(f"./videos/{video_id}", "rb") as video_file:
            video_content = video_file.read()
        return Response(content=video_content, headers=headers)
    elif video_id.endswith(".mp3"):
        headers["Content-Type"] = "video/mp3"
        headers["Content-Disposition"] = "attachment; filename=video.mp3"
        with open(f"./videos/{video_id}", "rb") as video_file:
            video_content = video_file.read()
        return Response(content=video_content, headers=headers)
    else:
        return {"message": "Invalid video type"}
