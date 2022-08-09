from flask import Blueprint, send_from_directory, request, abort, current_app as app
from flask_cors import cross_origin

from os.path import exists
from os import fsencode
from os import remove as remove_file

from project.database import Song
from project import db

import music_tag

library_blueprint = Blueprint("library", __name__)

@library_blueprint.route("/api/library/songs", methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def get_songs():

    
    songs = []
    information = {}

    for song in Song.query.all():
        songs.append(song.get_json())
        artist = song.artist
        album = song.album
        
        if artist not in information.keys():
            information[artist] = {"name": artist,
                                   "albums": {},
                                   "singles": []}

        if album == "":
            information[artist]["singles"].append(song.get_json())
        else:
            if album not in information[artist]["albums"].keys():
                information[artist]["albums"][album] = []
            information[artist]["albums"][album].append(song.get_json())        

            

    return {"songs": songs, "information": information}

@library_blueprint.route("/api/library/edit", methods=["POST"])
@cross_origin(origin="*", headers=['Content-Type'])
def edit_song():
    """ Edit a song

        Request: 
            data: The song information
        Responce: 
            success: if the song was modified
    """
    song_data = request.json["data"]
    
    song = Song.query.filter_by(id=int(song_data["song_id"])).first()

    song.title = song_data["title"]
    song.artist = song_data["artist"]
    song.album = song_data["album"]
    song.track = song_data["track"]

    song.rename(song.generate_filename(), True)
    song.update_tag()

    db.session.commit()

    return {"success": True}

@library_blueprint.route("/api/library/upload", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type'])
def upload_song():
    """ Upload a song """
    f = request.files['file']

    filename = app.config['MUSIC_DIR'] + "/" + f.filename

    f.save(filename)

    file_tags = music_tag.load_file(fsencode(filename))

    song = Song(str(file_tags["title"]), 
                str(file_tags["artist"]), 
                str(file_tags.get("album", "")), 
                str(file_tags.get("tracknumber","")), filename)
    
    song.rename(song.generate_filename(), overwrite=True)

    db.session.add(song)
    db.session.commit()
    
    return {"success": True}

@library_blueprint.route("/api/library/update_tag", methods=["GET"])
@cross_origin(origin='*', headers=['Content-Type'])
def update_tag():
    """ Update the tags on all songs in database """

    for song in Song.query.all():
        song.update_tag()

    db.session.commit()

    return {"success": True}

@library_blueprint.route("/api/library/delete/<song_id>", methods=['DELETE'])
@cross_origin(origin='*', headers=['Content-Type'])
def remove_song(song_id):
    """ Remove a song 

        Request: 
            song_id: The id of the song to remove
        Responce:
            success: If the song was removed
    """



    song = Song.query.filter_by(id=song_id).first()
    try:
        remove_file(song.filename)
    except:
        pass

    db.session.delete(song)
    db.session.commit()    

    return {"success": True}

@library_blueprint.route("/api/library/download/<path:path>")
@cross_origin(origin='*', headers=['Content-Type'])
def download_song(path):
    """ Download the song from the library """
    return send_from_directory(app.config["MUSIC_DIR"], path, as_attachment=True)


