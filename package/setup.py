""" Installing of the package """
from setuptools import setup, find_packages, Extension

setup(
        name='music_server',
        version='0.0.2',
        author='TheWorldOfCode',
        author_email='dannj75@gmail.com',
        packages=[
                    'music_server'
                ],
        install_requires=[
                    "flask",
                    "youtube-dl",
                    "youtube-search-python",
                    "music-tag",
                    "pysqlite3",
                    "pydub"
                ],
)
