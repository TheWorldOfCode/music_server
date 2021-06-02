""" Song """


class Song():

    """ A Song """

    def __init__(self, title="", album="", artist="", track=-1):
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

    def get_from_dict(self, info):
        """ Get the information from a dictionary

        :info: TODO
        :returns: TODO

        """
        self._title = info["title"]
        self._album = info["album"]
        self._artist = info["artist"]
        self._track = info["track"]

    def __str__(self) -> str:
        """ Return the song information in string format
        :returns: The song information

        """
        return self._title + "; " + self._album + "; " + self._artist + "; " + str(self._track) + ";"
