""" Handling youtube downloading """

from youtube_dl import YoutubeDL
from youtubesearchpython import Search
import os
import shutil
import music_tag
from time import sleep
from pydub import AudioSegment
from . import helper
from . import DataBase

DOWNLOAD_FOLDER = "./tmp"


class SearchError(Exception):
    """ A simple exception if there is a error when searching """
    pass


def search(word, limit=10):
    """
        Search the a word on youtube but only show the top limit results
    """
    result = Search(word, limit=limit)

    info = result.result()["result"]

    if len(info) == 0:
        raise SearchError()

    cleaned = []
    for i in info:
        cleaned.append({
            "title": i["title"],
            "url": i["link"],
            "type": i["type"],
            "duration": i.get("duration", ""),
            "count": i.get("videoCount", "")
        })

    return cleaned


class YoutubeDownloadLogger():
    """ """

    def debug(self, msg):
        """ """
        print(msg)

    def warning(self, msg):
        """ """
        print(msg)

    def error(self, msg):
        """ """
        print(msg)

    def progress(self, d):
        if d['status'] == "finished":
            print("HALLO")


def download(t: str, url: str, queue: str,) -> tuple:
    """
    Download from youtube

    :t: The type either video or playlist
    :url: The url for the video
    :queue: What there was seared for

    :return: A tuple contains an either a list or dict and the logger. If returned the list, it would contains a number dicts. Each dict contains information about each song downloaded

    """

    logger = YoutubeDownloadLogger()
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": DOWNLOAD_FOLDER + "/" + "%(title)s.%(ext)s",
        "audio-format": "m4a",
#        "logger": logger,
#        "progress_hooks": [logger.progress],
        }

    results = {}
    if t == "playlist":
        ydl_opts["outtmpl"] = DOWNLOAD_FOLDER + "/" + "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

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
                    "type": t,
                    "queue": queue
                })
                results = data
    elif t == "video":
        with YoutubeDL(ydl_opts) as ydl:
            information = ydl.extract_info(url, download=True)

            results = {
                "title": information.get("title", ""),
                "album": information.get("album", ""),
                "artist": information.get("uploader", ""),
                "filename": ydl.prepare_filename(information),
                "type": t,
                "queue": queue
            }

    return results, logger


def update_and_tag(db, tags):
    """ Update the database and the tags for the files """

    for file in tags:

        if file is None:
            continue

        album = file.get("album", "Single")
        if album == "":
            album = "Single"

        title = file.get("title", "").lstrip().rstrip()
        artist = file.get("artist", "").lstrip().rstrip()
        track = file.get("track", "").lstrip().rstrip()
        filename = file.get("filename", "")

        new_filename = artist + " - " + album + " - " + track + " - " + title + os.path.splitext(filename)[1]
        path = db._directory + "/" + artist + "/" + album + "/"

        new_filename = path + new_filename

        if not os.path.exists(path):
            print("CREATING PATH")
            os.makedirs(path)
        print(os.getcwd())
        #os.rename(os.fsencode(filename), os.fsencode(new_filename))
        shutil.move(os.fsencode(filename), os.fsencode(new_filename))

        if "m4a" not in new_filename:
            print("CONVERTING FILE")
            old_filename = new_filename
            name, externsion = os.path.splitext(new_filename)
            old = AudioSegment.from_file(new_filename,
                                         format=externsion.replace(".", ""))
            new_filename = name + ".m4a"
            old.export(new_filename, format="mp4")
            os.remove(os.fsencode(old_filename))

        f = music_tag.load_file(os.fsencode(new_filename))
        f['title'] = title
        f['album'] = album

        if track != "":
            f['tracknumber'] = track

        f['artist'] = artist
        f.save()

        db.add(new_filename)

    # Cleaning up
    helper.remove_empty_folders(DOWNLOAD_FOLDER)

def files_to_tag(info):
    """ Remove duplicates from the list and untracked files """
    print(info) 
    files = os.listdir(DOWNLOAD_FOLDER)
    missing = []
    
    def comp(file, info):
        print(info)
        if file == info["filename"]:
            return 1

        return 0

    for file in files:
        count = 0
        for tracked in info:
            if type(tracked) == list:
                for t in tracked:
                    count += comp(file, t)
            else:
                count += comp(file, tracked)

        if count == 0:
            missing.append(file)


    for file in missing:
        info.append({
            "title": file,
            "album": "",
            "artist": "",
            "filename": file,
            "type": "video",
            "queue": ""
        })

    return info
