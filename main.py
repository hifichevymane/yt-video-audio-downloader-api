from fastapi import FastAPI
from fastapi.responses import FileResponse
from schemas import YouTubeURL
import os
from pytube import YouTube
from random import randint

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Directory to upload all videos
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')


@app.post('/api/load_video/')
def load_video(video_url: YouTubeURL):
    yt = YouTube(video_url.url)
    video = yt.streams.get_highest_resolution()

    video_title = f'youtube_downloader_py_{randint(1, 100000)}'
    video_filename = f'{video_title}.mp4'
    # Creating file path for a video
    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, video_filename)

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Downloading
    video.download(output_path=UPLOAD_DIR, filename=video_filename)

    # Returning a download link
    return FileResponse(path=SAVE_FILE_PATH, filename=video_filename)
