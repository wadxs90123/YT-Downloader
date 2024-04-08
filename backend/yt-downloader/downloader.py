from pytube import YouTube
import uuid
from moviepy.editor import VideoFileClip
import os

def downloadVideo(url, type, outputPath=None):
    """
    Downloads a YouTube video from the given URL.
    
    Args:
        url (str): The URL of the YouTube video.
        type (str): The type of download file, can be MP4, WMV, or MP3.
        output_path (str, optional): The path to save the downloaded video file.
            If not provided, the video will be saved in the current directory.
    
    Returns:
        videoPath (str): The path where the video file was saved.
        videoName (str): Filename which is randomly generated.
    """
    videoName = str(uuid.uuid4())
    if type == "wmv":
        copy = videoName

    yt = YouTube(url)
    
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

    print("Video downloaded successfully")
    return videoName, videoPath

"""
if __name__ == "__main__":
    videoUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloadVideo(videoUrl)
"""