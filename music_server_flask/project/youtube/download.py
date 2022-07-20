from project import ext_celery
from flask import current_app as app

from youtube_dl import YoutubeDL
import logging

@ext_celery.celery.task
def download(url: str, type: str):
    
    folder = app.config["MUSIC_DIR"]

    logging.info(f"Starting downloading of {url}")
   # logger = YoutubeDownloadLogger()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": folder + "/" + "%(title)s.%(ext)s",
        "audio-format": "m4a",
        "quiet": True,
#        "logger": logger,
#        "progress_hooks": [logger.progress],
    }

    results = {}
    if type == "playlist":
        ydl_opts["outtmpl"] = folder + "/" + "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

        with YoutubeDL(ydl_opts) as ydl:
            information = ydl.extract_info(url, download=True)

            data = []
            for info in information["entries"]:
                data.append({
                    "title": info.get("title", ""),
                    "album": info.get("album", ""),
                    "track": info.get("playlist_index", ""),
                    "artist": info.get("artist", ""),
                    "filename": ydl.prepare_filename(info),
                    "type": type
                })
                results = data
    elif type == "video":
        with YoutubeDL(ydl_opts) as ydl:
            information = ydl.extract_info(url, download=True)

            results = [{
                "title": information.get("title", ""),
                "album": information.get("album", ""),
                "artist": information.get("uploader", ""),
                "filename": ydl.prepare_filename(information),
                "type": type
            }]

    logging.info(f"Downloading of {url} is done.")
    
    return results