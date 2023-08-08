from fastapi import FastAPI
from fastapi.responses import FileResponse
from schemas import YouTubeURL
import os
import utils


app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Directory to upload all videos
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')


# Downloading a video
@app.post('/api/get_video/')
def get_video(video_url: YouTubeURL):
    file_info = utils.download_video(video_url=video_url.url)
    # Returning a download link
    return FileResponse(path=file_info.path, filename=file_info.name)


# Downloading a audio
@app.post('/api/get_audio/')
def get_audio(video_url: YouTubeURL):
    file_info = utils.download_audio(video_url=video_url.url)
    # Returning a download link
    return FileResponse(path=file_info.path, filename=file_info.name)
