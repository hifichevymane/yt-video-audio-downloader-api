from dataclasses import dataclass
from pytube import YouTube
from random import randint
import os
import main
import subprocess


# Dataclass of downloaded file info
@dataclass
class FileInfo:
    path: str
    name: str


# Downloading a video func
def download_video(video_url: str) -> FileInfo:
    """Download video with YouTube video URL"""

    yt = YouTube(video_url)
    video = yt.streams.get_highest_resolution()

    video_title = f'youtube_downloader_py_{randint(1, 100000)}'
    video_filename = f'{video_title}.mp4'
    # Creating file path for a video
    SAVE_FILE_PATH = os.path.join(main.UPLOAD_DIR, video_filename)

    if not os.path.exists(main.UPLOAD_DIR):
        os.makedirs(main.UPLOAD_DIR)

    # Downloading
    video.download(output_path=main.UPLOAD_DIR, filename=video_filename)

    # Returning an dataclass FileInfo with all file information
    return FileInfo(path=SAVE_FILE_PATH, name=video_filename)


# Downloading an audio
def download_audio(video_url: str, delete_video: bool = False) -> FileInfo:
    """Download an audio of YouTube video converting MP4 to MP3"""

    downloaded_file = download_video(video_url)
    # Convert mp4 to mp3
    # mp4_file_path = os.path.join(
    #     downloaded_file.path, f'{downloaded_file.name}')

    # Making file name and path to the file
    mp3_file_name = f'{downloaded_file.name[:-4]}.mp3'
    mp3_file_path = os.path.join(main.UPLOAD_DIR, mp3_file_name)

    # Creating an ffmpeg command and execute it
    cmd = f'ffmpeg -i "{downloaded_file.path}" -vn -ab 320k "{mp3_file_path}"'
    subprocess.call(cmd, shell=True)

    if delete_video:
        os.remove(downloaded_file.path)

    return FileInfo(path=mp3_file_path, name=mp3_file_name)
