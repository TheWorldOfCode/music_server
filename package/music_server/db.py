""" Handle the data base """
from typing import List
import logging
import sqlite3 as db
from sqlite3 import Error
from os.path import isfile, join
from os import listdir
from pathlib import Path

from .song import load_song, Song
from threading import Lock

class NoResult(Exception):
    pass

class InvalidQueue(Exception):
    pass

database = None

class DataBase(object):

    """ Handles the music database"""

    def __init__(self, directory, db_file):
        """ Create the music datacase

        :directory: The directory containing the music
        :db_file: the file containing the database

        """
        self.mutex = Lock()

        if isfile(db_file):
            self.load(db_file)
        else:
            self.new(db_file)

        self._directory = directory
        self.update()
        self.save()

    def new(self, file: str):
        """ Create a new database

        :file: TODO
        :returns: TODO

        """
        self.mutex.acquire()
        try:
            self._conn = db.connect(file)

            cursor = self._conn.cursor()
            TABLE = """CREATE TABLE song (
                        songid integer PRIMARY KEY,
                        filename text NOT NULL,
                        modified integer NOT NULL,
                        artist text,
                        album text,
                        title text NOT NULL,
                        track text);
            """
            cursor.execute(TABLE)

            TABLE = """ CREATE TABLE download (
                        download_id integer PRIMARY KEY,
                        linked integer,
                        filename text NOT NULL,
                        artist text,
                        album text,
                        title text NOT NULL,
                        track text);
                     """
            cursor.execute(TABLE)
        except Error as e:
            logging.error(e)

        self.mutex.release()

    def load(self, file: str):
        """ Load a database file

        :file: TODO
        :returns: TODO

        """
        self._conn = None
        self.mutex.acquire()

        try:
            self._conn = db.connect(file)
        except Error as e:
            logging.error(e)
            
        self.mutex.release()

    def save(self) -> None:
        """ Save the database to the file

        :returns: TODO

        """
        self.mutex.acquire()
        self._conn.commit()
        self.mutex.release()

    def get_tables(self) -> list:
        """ Get the tables in database """
        self.mutex.acquire()
        cursor = self._conn.cursor()

        data = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        self.mutex.release()

        table = []
        for t in data:
            table.append(t[0])
        
        return table

    def add_download(self, info) -> None:
        """ Add a download two database """
        self.mutex.acquire()
        cursor = self._conn.cursor()

        if type(info) == list:
            flag = False
            id = 0
            for entry in info:

                if flag:
                    INSERT = """INSERT INTO download (linked, filename, artist, album, title, track) VALUES (?, ?, ?, ?, ?, ?)"""
                    data = (id, entry["filename"], entry["artist"], entry["album"], entry["title"], entry["track"])
                    cursor.execute(INSERT, data)
                else:
                    INSERT = """INSERT INTO download (filename, artist, album, title, track) VALUES (?, ?, ?, ?, ?)"""
                    data = (entry["filename"], entry["artist"], entry["album"], entry["title"], entry["track"])
                    cursor.execute(INSERT, data)
                    flag = True
                    id = cursor.lastrowid 

        else:
            INSERT = """INSERT INTO download (filename, artist, album, title, track) VALUES (?, ?, ?, ?, ?)"""
            data = (info["filename"], info["artist"], info["album"], info["title"], info["track"])
            cursor.execute(INSERT, data)

        self.mutex.release()

    def count_download(self) -> int:
        """ Count the number of files downloaded """
        self.mutex.acquire()

        cursor = self._conn.cursor()

        sql = "SELECT count(*) FROM download"

        count = cursor.execute(sql).fetchall()[0][0]

        self.mutex.release()

        return count

    def get_download_info(self):
        """ Get info for all entries in download table
            Only gets the first entry for a playlist/album
        """
        self.mutex.acquire()
        cur = self._conn.cursor()

        SELECT = """SELECT download_id, linked, title FROM download """

        data = cur.execute(SELECT).fetchall()

        if len(data) == 0:
            self.mutex.release()
            return []

        d = []
        for entry in data:
            if entry[1] is None:
                d.append(entry)

        self.mutex.release()

        return d

    def get_download(self):
        """ Get all entries in download table """
        self.mutex.acquire()
        cur = self._conn.cursor()

        SELECT = """SELECT * FROM download """

        data = cur.execute(SELECT).fetchall()

        if len(data) == 0:
            self.mutex.release()
            return []
        
        self.mutex.release()

        return data

    def tag_download(self, index):
        """ Get info for index and remove it """
        self.mutex.acquire()
        cursor = self._conn.cursor() 

        SELECT = f"SELECT * FROM download WHERE download_id={index}"

        data = cursor.execute(SELECT).fetchall()

        DELETE = f"DELETE FROM download WHERE download_id={index}"
        cursor.execute(DELETE)

        self.mutex.release()

        self.save()

        return data

    def add(self, filename, table="song") -> None:
        """ Add song to database

        :filename: TODO
        :returns: TODO

        """
        self.mutex.acquire()
        cursor = self._conn.cursor()

        INSERT = """INSERT INTO song (
        filename, modified, artist, album, title, track) VALUES
        (?, ?, ?, ?, ?, ?)
        """

        mtime = Path(filename).stat().st_ctime

        song = load_song(filename)
        data = (filename, mtime, song.get_artist(), song.get_album(), song.get_title(), song.get_track())
        cursor.execute(INSERT, data)
        self.mutex.release()

    def remove(self, filename):
        """ Remove a song from the database

        :filename: TODO
        :returns: TODO

        """
        self.mutex.acquire()
        sql = 'DELETE FROM song WHERE filename=?'

        cur = self._conn.cursor()
        cur.execute(sql, (filename,))
        self.mutex.release()

    def update_file(self, file):
        """ Update the file in database

        :file: TODO
        :returns: TODO

        """
        pass

    def _get_songs_dir(self, directory) -> dict:
        """ Get all songs in a directory

        :directory: TODO
        :returns: TODO

        """
        songs = {}
        for elm in listdir(directory):

            fullpath = join(directory, elm)

            if isfile(fullpath):
                songs[fullpath] = Path(fullpath).stat().st_ctime

            else:
                songs = {**songs, **self._get_songs_dir(fullpath)}

        return songs

    def update(self, directory=None) -> None:
        """ Update the database

        :directory: TODO
        :returns: TODO

        """

        if directory is None:
            directory = self._directory

        fdb = self._get_songs_dir(directory)

        cursor = self._conn.cursor()
        db = cursor.execute("SELECT filename, modified FROM song").fetchall()

        if len(db) == 0:
            for file in fdb.keys():
                self.add(file)

            return

        db_filenames = []
        for f, t in db:
            new_time = fdb.get(f, None)

            if new_time is None:
                self.remove(f)
            else:
                db_filenames.append(f)
                #            elif new_time != t:
                    #               self.update_file(f)

        for f in fdb.keys():
            if f not in db_filenames:
                self.add(f)

    def search(self, word: dict) -> List[Song]:
        """ Search for a song in the 

        :word: Dictory with either title, artits, album, track
        :returns: The possible songs

        """
        self.mutex.acquire()
        cursor = self._conn.cursor()

        condinations = []

        for key in word.keys():
            if key in ["songid", "title", "artist", "album", "track"]:
                condinations.append(f"{key}=\'{word[key]}\'")

        if len(condinations) == 0:
            self.mutex.release()
            raise InvalidQueue

        condination = "SELECT * FROM song WHERE "
        for i in range(len(condinations) -1):
            condination += condinations[i] + " AND "
            condination += condinations[-1]

        try:
            db = cursor.execute(condination).fetchall()
        except Error as e:
            logging.error(f"Search string {condination}, Error {e}")
            self.mutex.release()
            raise NoResult

        if len(db) == 0:
            self.mutex.release()
            raise NoResult

        songs = []
        for i, filename, _, ar, al, ti, tr  in db:
            songs.append(Song(id=i, title=ti, album=al, artist=ar, track=tr,
                              filename=filename))
            self.mutex.release()

        return songs

    def get_unique_tag(self, tag, filter=None, order=None, asc=False) -> List[str]:
        """ Get the unique tag of the system
        :tag: Tag to use 
        :return: A unique list of values from the tag
        """
        self.mutex.acquire()
        if type(tag) == str:
            sql = f"SELECT DISTINCT {tag} FROM song"
        else:
            elm = ""
            for i in range(len(tag) - 1):
                elm += f"{tag[i]}, "
                elm += tag[-1]

            sql = f"SELECT DISTINCT {elm} FROM song"

        if filter != None:
            sql += " WHERE "

            condinations = []
            for key in filter.keys():
                if key in ["title", "artist", "album", "track"]:
                    condinations.append(f"{key}=\'{filter[key]}\'")

            for i in range(len(condinations) -1):
                sql += condinations[i] + " AND "

            sql += condinations[-1]

        if order != None:
            sql += " ORDER BY "

            for i in range(len(order) - 1):
                sql += f"{order[i]}, "
                sql += f"{order[-1]}"

            if asc:
                sql += " ASC"
            else:
                sql += " DESC"

        cursor = self._conn.cursor()

        _tags = cursor.execute(sql).fetchall()

        tags = []

        for t in _tags:
            if len(t) == 1:
                tags.append(t[0])
            else:
                k = {}
                for i in range(len(tag)):
                    k[tag[i]] = t[i]

                tags.append(k)

        self.mutex.release()

        return tags

    def empty(self) -> bool:
        """ Check if the database is empty """
        flag = True
        self.mutex.acquire()
        cur = self._conn.cursor()

        sql = "SELECT count(*) FROM song"

        k = cur.execute(sql).fetchall()[0][0]

        if k != 0:
            flag = False

        self.mutex.release()

        return flag

def get_database() -> DataBase:
    global database
    return database

def create_database(directory, db_file):
    global database
    database = DataBase(directory, db_file)

def main():
    db = DataBase("/home/dajak/Music", "tests/test.db")
    db.empty()


if __name__ == "__main__":
    main()
