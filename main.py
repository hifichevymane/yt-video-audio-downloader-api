from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import utils
from pydantic import BaseModel
import uvicorn


# Schema
class YouTubeURL(BaseModel):
    url: str


app = FastAPI()

# Creating static files directory
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Directory to upload all videos
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

# Allow React app to send API requests
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "localhost:3000",
]

# Adding CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Downloading a video
@app.post('/api/get_video/')
def get_video(video_url: YouTubeURL):
    file_info = utils.download_video(video_url=video_url.url)
    # Returning a download link
    return {'file_path': f'http://127.0.0.1:8000/uploads/{file_info.name}'}


# Downloading a audio
@app.post('/api/get_audio/')
def get_audio(video_url: YouTubeURL):
    file_info = utils.download_audio(video_url=video_url.url)
    # Returning an answer with download link
    return {'file_path': f'http://127.0.0.1:8000/uploads/{file_info.name}'}


# Running uvicorn server when run the script
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
