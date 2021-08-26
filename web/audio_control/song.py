""" Song """


class Song():

    """ A Song """

    def __init__(self, id=-1, title="", album="", artist="", track=-1):
        """TODO: to be defined.

        :title: TODO
        :album: TODO
        :artist: TODO
        :track: TODO

        """
        self._title = title
        self._album = album
        self._artist = artist
        self._track = track
        self._id = id
        self._current = False

    def get_title(self) -> str:
        """ get the title
        :returns: Return the title

        """
        return self._title

    def get_track(self) -> str:
        """ Get the track number
        :returns: Return the track number

        """
        return str(self._track)

    def get_artist(self) -> str:
        """ Get the artist
        :returns: The artist

        """
        return self._artist

    def get_album(self):
        """ Get the album
        :returns: Return the album

        """
        return self._album

    def get_title_track(self) -> str:
        """ Return a combine string with the track number and title
        :returns: Return the combined string

        """
        if self._track == -1:
            return self.get_title()
        return "{} - {}".format(self._track, self._title)

    def get_album_artist(self):
        """ Get a combined string with the album and artist
        :returns: the string

        """
        if self._album == "":
            return self.get_album()
        return "{} - {}".format(self._album, self._artist)

    def get_from_dict(self, info):
        """ Get the information from a dictionary

        :info: TODO
        :returns: TODO

        """
        self._title = info.get("title", "")
        self._album = info.get("album", "")
        self._artist = info.get("artist", "")
        self._track = info.get("track", "")
        self._id = info.get("id", "")

    def get_id(self) -> int:
        """ Get the id of the song
        :returns: The id

        """
        return self._id

    def set_current(self):
        """  Mark the song as the current playing song
        :returns: TODO

        """
        self._current = True

    def __str__(self) -> str:
        """ Return the song information in string format
        :returns: The song information

        """
        return self._title + "; " + self._album + "; " + self._artist + "; " + str(self._track) + ";"


class Playlist(object):

    """ Handle a playlist """

    def __init__(self):
        """TODO: to be defined. """
        self.songs = []

    def load(self, list: dict, current_id=-1):
        """ Load playlist

        :list: The playlist from mpd playlistinfo
        :current_id: The index of the current playing song

        """
        for song_info in list:
            song = Song()
            song.get_from_dict(song_info)
            self.songs.append(song)

        current_id = int(current_id)
        if len(self.songs) < current_id or current_id < 0:
            return

        self.songs[current_id].set_current()
