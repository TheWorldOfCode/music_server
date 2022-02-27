import unittest
from music_server import DataBase
from os import mkdir, remove
from os.path import exists


class TestDB(unittest.TestCase):

    def test_song_table(self):
        """ Test if the song table is created """
        db = DataBase("/tmp/music", "/tmp/music_test_1.db")

        tables = db.get_tables()
        
        return self.assertIn("song", tables)

    def test_download_table(self):
        """ Test if the song table is created """
        db = DataBase("/tmp/music", "/tmp/music_test_2.db")

        tables = db.get_tables()
        
        return self.assertIn("download", tables)

    def test_add_download_single(self):
        """ Test if it is possible to add a single song to the download database """
        db = DataBase("/tmp/music", "/tmp/music_test_3.db")

        info = {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song", "track": 0 }

        db.add_download(info)

        count = db.count_download()
        
        return self.assertEqual(count, 1, "Failed to add download")

    def test_add_download_album(self):
        """ Test if it is possible to add an album/playlist to the download database """
        db = DataBase("/tmp/music", "/tmp/music_test_4.db")

        info = [
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 2", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 3", "track": 0 }
        ]

        db.add_download(info)
        
        count = db.count_download()
        
        return self.assertEqual(count, 3, "Failed to add all songs from album to download")

    def test_get_download_info(self):
        """ Test if getting the correct number of entries for displaing """
        db = DataBase("/tmp/music", "/tmp/music_test_5.db")

        info = [
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 2", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 3", "track": 0 }
        ]

        db.add_download(info)

        info = {"filename": "test", "artist": "test", "album": "test", "title": "This is a test song", "track": 0 }

        db.add_download(info)

        data = db.get_download_info()
        
        return self.assertEqual(len(data), 2, "Got a wrong number of entries in the information")

    def test_get_download(self):
        """ Test if if possible to get all entries in download"""
        db = DataBase("/tmp/music", "/tmp/music_test_6.db")

        info = [
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 2", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 3", "track": 0 }
        ]

        db.add_download(info)

        info = {"filename": "test", "artist": "test", "album": "test", "title": "This is a test song", "track": 0 }

        db.add_download(info)

        data = db.get_download()
        
        return self.assertEqual(len(data), 4, "Got a wrong number of entries from the database")

    def test_tag_download(self):
        """ Test if getting the right number of entries when desired to tag"""
        db = DataBase("/tmp/music", "/tmp/music_test_6.db")

        info = [
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 2", "track": 0 },
            {"filename": "test", "artist": "test2", "album": "test", "title": "This is a test song 3", "track": 0 }
        ]

        db.add_download(info)

        info = {"filename": "test", "artist": "test", "album": "test", "title": "This is a test song", "track": 0 }

        db.add_download(info)

        data = db.tag_download(1)

        cnt = len(data)

        cnt += len(db.tag_download(4))
        
        return self.assertEqual(cnt, 4, "Got a wrong number of entries from the database")

if __name__ == "__main__":
    if not exists("/tmp/music"):
        mkdir("/tmp/music")
    unittest.main()
  #  remove("/tmp/music")
  #  remove("/tmp/music_test.db")