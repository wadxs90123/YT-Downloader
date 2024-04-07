from pytube import YouTube

def downloadVideo(url, outputPath=None):
    """
    Downloads a YouTube video from the given URL.
    
    Args:
        url (str): The URL of the YouTube video.
        output_path (str, optional): The path to save the downloaded video file.
            If not provided, the video will be saved in the current directory.
    
    Returns:
        str: The path where the video file was saved.
    """
    yt = YouTube(url)
    
    # Get the highest resolution video stream
    videoStream = yt.streams.filter(progressive=True).get_highest_resolution()
    
    if outputPath:
        videoPath = outputPath
    else:
        videoPath = videoStream.default_filename
    
    # Download the video
    videoStream.download()
    
    print(f"Video downloaded successfully: {videoPath}")
    return videoPath

"""
if __name__ == "__main__":
    videoUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloadVideo(videoUrl)
"""