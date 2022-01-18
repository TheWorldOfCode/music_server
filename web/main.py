""" """
import logging
from flask import Flask, render_template, request, redirect, url_for, send_file
from mpd import MPDClient, ConnectionError
from music_server import Song, Playlist 
from music_server import search, download, update_and_tag, DOWNLOAD_FOLDER
from music_server import remove_empty_folders, db_update
from music_server import ProcessHandler
from music_server import DataBase, NoResult, InvalidQueue
import json
import os

MUSIC_DIR = "./static/music"

app = Flask(__name__)
processHandler: ProcessHandler = ProcessHandler()

PLAYLIST_NAME = "Unnamed"

def connect():
    pass
    client = MPDClient()
    try:
        client.connect("localhost", 6600)
    except ConnectionError:
        pass

    return client


@app.route("/", methods=["POST", "GET"])
def playlist():
    return redirect(url_for("library"))
    client = connect()
    status = client.status()
    current_song: Song = Song()
    current_song.get_from_dict(client.currentsong())
    playlist_info = client.playlistinfo()
    print(status)
    if len(playlist_info) == 0:
        return redirect(url_for("library"))

    current_playlist: Playlist = Playlist()

    if "song" in status:
        current_playlist.load(playlist_info, status["song"])
    else:
        current_playlist.load(playlist_info)

    client.disconnect()
    return render_template("playlist.html",
                           title=current_song.get_title_track(),
                           artist=current_song.get_album_artist(),
                           playlist=current_playlist)


@app.route("/library")
def library():
    global MUSIC_DIR
    db = DataBase(MUSIC_DIR, "music.db")

    if db.empty():
        return redirect(url_for("youtube_downloader"))

    current_song: Song = Song()

    playlists = []

    artists = db.get_unique_tag("artist")

    return render_template("library.html",
                           title=current_song.get_title_track(),
                           artist=current_song.get_album_artist(),
                           playlists=playlists,
                           artists=artists)


@app.route("/youtube_downloader")
def youtube_downloader():
    return render_template("youtube.html")


@app.route("/youtube_downloader_control")
def downloader_control():
    global processHandler
    action = request.args.get('action', "", type=str)

    ret = ""
    if action == "search":
        queue = request.args.get("queue", "", type=str)
        nr = request.args.get("hits", 10, type=int)

        result = search(queue, nr)

        ret = {
            "action": action,
            "result": result
        }

    elif action == "download":
        tp: str = request.args.get("type", "", type=str)
        queue: str = request.args.get("queue", "", type=str)
        url: str = request.args.get("url", "", type=str)

        print("starting Downloading")

        processHandler.start_process(target=download, args=(tp, url, queue),
                                     job_info=queue)

    elif action == "tag":
        tp: str = request.args.get("type", "", type=str)
        details = json.loads(request.args.get("details", ""))

        client = connect()
        update_and_tag(client, details)

        client.disconnect()
    elif action == "tag_editor":
        pid = request.args.get("id", -1, type=int)

        if pid != -1:
            res = processHandler.join(pid)
            ret = res[0][0]

            processHandler.cleanup(pid)
        else:
            ret = "nothing"
    return ret


@app.route('/player_control')
def player_control():
    global PLAYLIST_NAME
    client = connect()
    mpd_status = client.status()
    status = request.args.get('status', "", type=str)

    ret = "nothing"
    if status == "play":
        print(mpd_status)
        if mpd_status['state'] == "play":
            client.pause(1)
            ret = {"status": "paused"}
        elif mpd_status['state'] == "stop":
            client.play(0)
            ret = {"status": "play"}
        else:
            client.pause(0)
            ret = {"status": "play"}
    elif status == "next":
        client.next()
    elif status == "prev":
        client.previous()
    elif status == "playlist":
        action = request.args.get('action', "", type=str)
        song_id = request.args.get('song', "", type=int)
        if action == "play":
            client.playid(song_id)
        elif action == "remove":
            PLAYLIST_NAME = "Unnamed"
            client.deleteid(song_id)
    elif status == "suffle":
        client.shuffle()
    elif status == "random":
        client.random((int(mpd_status['random']) + 1) % 2)
    elif status == "repeat":
        client.repeat((int(mpd_status['repeat']) + 1) % 2)
    elif status == "consume":
        client.consume((int(mpd_status['consume']) + 1) % 2)
    elif status == "clear":
        client.clear()
        ret = url_for("/library")
    elif status == "song":
        ret = client.currentsong()
    elif status == "save":
        name = request.args.get("name", "", type=str)
        client.save(name)

    client.disconnect()

    return ret


@app.route('/queue')
def queue():
    """ Queue for data.
    :returns: TODO

    """
    global PLAYLIST_NAME, MUSIC_DIR
    db = DataBase(MUSIC_DIR, "music.db")

    type = request.args.get('type', "", type=str)
    info: str = request.args.get('info', "", type=str)

    #if type == "" or info == "":
    #    client.disconnect()
    #    return "Error"


    html = "Error"
    if type == "Album":
         html = db.get_unique_tag("album", {"artist": info})
    elif type == "Title":
        html = db.get_unique_tag(["title", "track"], {"album": info}, ["track"], True)
    elif type == "add":
        pass
#        info = info.split("_")

#        if info[0] == "playlist":
#            PLAYLIST_NAME = info[1]
#        else:
#            PLAYLIST_NAME = "Unnamed"
#
#        if len(info) == 2 and info[0] == "playlist":
#            client.load(info[1])
#            html = "Playing playlist"
#        elif len(info) == 2 and info[0] == "artist":
#            artist = info[1]
#            songs = client.find("artist", artist)
#            if len(songs) != 0:
#                html = "Songs added"
#                for song in songs:
#                    client.add(song["file"])
#            else:
#                html = "Error: Songs not added"
#        elif len(info) == 4:
#            artist = info[1]
#            album = info[3]
#
#            songs = client.find("artist", artist, "album", album)
#            if len(songs) != 0:
#                html = "Songs added"
#                for song in songs:
#                    client.add(song["file"])
#            else:
#                html = "Error: Songs not added"
#        else:
#            artist = info[1]
#            album = info[3]
#            song = info[5]
#
#            songs = client.find("artist", artist, "album", album, "title", song)
#            if len(songs) != 0:
##                html = "Songs added"
#                for song in songs:
#                    client.add(song["file"])
#            else:
#                html = "Error: Songs not added"
    elif type == "remove":
        info = info.split("_")
        word = {}
        for i in range(0, len(info), 2):
            word[info[i]] = info[i + 1]

        try:
            results = db.search(word)
            for song in results:
                os.remove(os.fsencode(song.get_filename()))
                db.remove(song.get_filename())

            db.save()
            html = "Songs removed"
        except NoResult: 
            logging.error("Queue::remove : No result in database")
            html = "Error: Songs not removed"
        except InvalidQueue:
            logging.error("Queue::remove : Invalid SQL queue")
            html = "Error: Songs not removed"
    elif type == "download":
        info = info.split("_")
        word = {}
        for i in range(0, len(info), 2):
            word[info[i]] = info[i + 1]

        try:
            results = db.search(word)
            filenames = []
            for song in results:
                filenames.append(song.get_filename().replace("/", "!_!"))

            html = filenames
        except NoResult: 
            logging.error("Queue::remove : No result in database")
        except InvalidQueue:
            logging.error("Queue::remove : Invalid SQL queue")

#        if len(info) == 2 and info[0] == "playlist":
    #            client.rm(info[1])
    #            html = "Playlist removed"
    #if len(info) == 2 and info[0] == "artist":
        #            artist = info[1]
        #            songs = client.find("artist", artist)
        #            if len(songs) != 0:
            #                html = "Songs removed"
            #                for song in songs:
                #            os.remove(os.fsencode(DOWNLOAD_FOLDER + "/" + song['file']))
                #            else:
                    #               html = "Error: Songs not removed"
                    #elif len(info) == 4:
                        #    artist = info[1]
                        #    album = info[3]
                        #
                        #            songs = client.find("artist", artist, "album", album)
                        #            if len(songs) != 0:
                            #                html = "Songs removed"
                            #                for song in songs:
                                #                    os.remove(os.fsencode(DOWNLOAD_FOLDER + "/" + song['file']))
                                #            else:
                                    #                html = "Error: Songs not removed"
                                    #        else:
                                        #            artist = info[1]
                                        #            album = info[3]
                                        #            song = info[5]
                                        #
                                        #            songs = client.find("artist", artist, "album", album, "title", song)
                                        #            print(songs)
                                        #            if len(songs) != 0:
                                            #                html = "Songs removed"
                                            #                for song in songs:
                                                #                    os.remove(os.fsencode(DOWNLOAD_FOLDER + "/" + song['file']))
                                                #            else:
                                                    #                html = "Error: Songs not removed"

#        remove_empty_folders(DOWNLOAD_FOLDER)
#        db_update(client, 0)

#    client.disconnect()

    return dict(data=html)

@app.route("/download_music/<filename>")
def download_music(filename):
    filename = filename.replace("!_!", "/")
    print(filename)
    return send_file(filename, as_attachment=True)

@app.route("/status")
def status():
    global processHandler, PLAYLIST_NAME
    #client = connect()

    #mpd_status = client.status()

    action = request.args.get('action', "", type=str)
    ret = "nothing"

    if action == "song":
        pass
    #    ret = {"song": "", "status": ""}
    elif action == "playlist":
        pass
    #    print(PLAYLIST_NAME)
    #    ret = {"name": PLAYLIST_NAME}
    elif action == "downloading":
        if processHandler.count() > 0:
            status = processHandler.status()
            running = 0
            finished = 0
            job_info = []

            for s in status:
                if "RUNNING" in s:
                    running += 1
                else:
                    info = processHandler.get_info(int(s.split(" ")[0]))
                    job_info.append([info, s.split(" ")[0]])
                    finished += 1

            ret = {"running": running, "finished": finished, "info": job_info}
        else:
            ret = {"running": 0, "finished": 0}

#    client.disconnect()

    return ret


if __name__ == "__main__":
    DataBase(MUSIC_DIR, "music.db")
    app.run(host="0.0.0.0", debug=True)
