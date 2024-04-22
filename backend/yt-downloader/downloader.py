from pytube import YouTube
import uuid
from moviepy.editor import VideoFileClip
import os
import threading
import socket
import websocket

progress = 0
id = ""
def sendprogress() :
    # Create WebSocket connection
    ws_uri = 'ws://localhost:8765'
    ws = websocket.WebSocket()
    ws.connect(ws_uri)
    # 发送消息给服务器
    response_string = str(progress) + "," + id
    ws.send( response_string )
    ws.close()

def onprogress(stream, chunk, remains):
    global progress
    total = stream.filesize                     # 取得完整尺寸
    percent = (total - remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
    print(f'下載中… {percent:05.2f}')  # 顯示進度，\r 表示不換行，在同一行更新
    progress = int(percent)

    sendprogress()

def downloadVideo(url, type, clent_id, outputPath=None):
    """
    Downloads a YouTube video from the given URL.
    
    Args:
        url (str): The URL of the YouTube video.
        type (str): The type of download file, can be MP4, WMV, or MP3.
        output_path (str, optional): The path to save the downloaded video file.
            If not provided, the video will be saved in the current directory.
        clent_id (str): The client id.
    
    Returns:
        videoPath (str): The path where the video file was saved.
        videoName (str): Filename which is randomly generated.
        originalTitle (str): The original title of the YouTube video.
    """
    
    global progress
    progress = 0
    global id
    id = clent_id
    sendprogress()

    videoName = str(uuid.uuid4())
    if type == "wmv":
        copy = videoName
    yt = YouTube(url , on_progress_callback = onprogress)
    originalTitle = yt.title

    # Get the highest resolution video stream
    if type == "mp4" or type == "wmv":
        # Add the file format after the video name based on type
        videoName += ".mp4"
        videoStream = yt.streams.filter(progressive=True).get_highest_resolution()
    elif type == "mp3":
        videoName += ".mp3"
        videoStream = yt.streams.filter(only_audio=True).first()

    # Download the video
    if outputPath:
        videoPath = outputPath
        videoStream.download(output_path=outputPath, filename=videoName)
    else:
        videoPath = os.getcwd()
        videoStream.download(filename=videoName)

    if(type == "wmv") :
        progress = 99
    sendprogress()

    # Use moviepy to convert video file from MP4 to WMV
    if type == "wmv":
        if outputPath:
            videoName = outputPath + "/" + videoName
            VideoFileClip(videoName).write_videofile(f"{outputPath}/{copy}.wmv",temp_audiofile="temp-audio.m4a", remove_temp=True, codec="wmv2", audio_codec="aac")
        else:
            VideoFileClip(videoName).write_videofile(f"{copy}.wmv",temp_audiofile="temp-audio.m4a", remove_temp=True, codec="wmv2", audio_codec="aac")
        if os.path.exists(videoName):
            os.remove(videoName)
        videoName = copy + ".wmv"

    sendprogress()
    print("Video downloaded successfully")
    return videoName , videoPath , originalTitle

"""
if __name__ == "__main__":
    videoUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloadVideo(videoUrl)
"""