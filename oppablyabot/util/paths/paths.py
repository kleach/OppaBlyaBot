import os
import sys


def mkdir(path: str):
    if os.path.exists(path) and os.path.isdir(path):
        return

    os.mkdir(path)


def _dirpath_impl(root_path: str, *args) -> str:
    return os.path.normpath(os.path.join(root_path, *args))


PROJECT = os.path.normpath(os.path.dirname(sys.argv[0]))


def projectpath(*args) -> str:
    return _dirpath_impl(PROJECT, *args)


DOT_ENV = projectpath('.env')

DATA = projectpath('data')
mkdir(DATA)


def datapath(*args) -> str:
    return _dirpath_impl(DATA, *args)


MEDIA = datapath('media')
mkdir(MEDIA)


def mediapath(filename: str) -> str:
    return _dirpath_impl(MEDIA, filename)


JOINED_MEDIA_SRC = mediapath('joined.mp4')
LEFT_MEDIA_SRC = mediapath('left.mp4')
