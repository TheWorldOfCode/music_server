from project import db
from flask import current_app as app

import shutil
import os.path as path
from os import mkdir, fsencode

import music_tag

class Song(db.Model):
    """ Handle a song in the database """
    __tablename__="songs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)
    album = db.Column(db.Text)
    track = db.Column(db.Text)
    filename = db.Column(db.Text, nullable=False)

    def __init__(self, title, artist, album, track, filename):
        """ Create a Song object
            
            @param title The title of the song
            @param artist The artist of the song
            @param album Which album the song belongs to
            @param track The songs track number on the album
            @param filename Filename of the song

        """
        self.title = title
        self.artist = artist
        self.album = album
        self.track = track
        self.filename = filename.replace(app.config["MUSIC_DIR"] + "/", "")


    def check_filename(self, overwrite=False):
        """ Check if the filename corresponds with information 
            and corrected the filename

            @param overwrite Overwrite existing files
        """

        if self.generate_filename() != self.filename:
            self.rename(self.generate_filename())
        

    def generate_filename(self) -> str:
        """ Generate the file name according to the 
            title, artist, album and track

            @return The filename
        """
        
        filename = self.artist + "/" 
        if self.album != "":
            filename += self.album + "/" 
        
        if self.track != "":
            filename += self.track + "-" 
        
        filename += self.title 
        filename += "." + self.filename.split(".")[1]
        return filename

    def rename(self, new_name, overwrite=False):
        """ Rename the file 

        @param new_name The new file name

        """
        new_name2 = new_name
        new_name = fscode(app.config["MUSIC_DIR"] + "/" + new_name)

        if not path.exists(path.dirname(new_name)):
            mkdir(path.dirname(new_name))
        
        if path.exists(new_name):
            raise RuntimeError("File already exists")
        
        shutil.move(fscode(app.config["MUSIC_DIR"] + "/" + self.filename), new_name)

        self.filename = new_name2

    def get_json(self) -> dict:
        """ Get the data element as a dict 

            @return The json representation
        """

        return {
                "song_id": self.id,
                "title": self.title,
                "artist": self.artist,
                "album": self.album,
                "track": self.track,
                "filename": self.filename
               }

    def update_tag(self) -> None:
        """ Update the tags on the song """
        song = music_tag.load_file(app.config["MUSIC_DIR"] + "/" + self.filename)

        song["title"] = self.title
        
        song["album"] = self.album
        song["artist"] = self.artist
        if self.track == "":
            song["tracknumber"] = None 
        else:
            song["tracknumber"] = int(self.track)

        song.save()