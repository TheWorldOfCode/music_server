""" Handle the data base """
from typing import List
def get_artists(info):
    """ Get the list of artist convert the raw information into strings

    :info: TODO
    :returns: TODO

    """
    return [ a["artist"] for a in info ]

def get_album_element(info):
    """ Create the html elements for album

    :info: TODO
    :returns: TODO

    """
    album: List[str] = [ a["album"] for a in info ]
    return album
