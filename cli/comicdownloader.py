#!env python
# --*-- encoding: iso-8859-1 --*--
"""
comicdownloader : download de comics
"""

import sys
sys.path.insert(0, '../src/')
sys.path.insert(0, '../src/core/')

from argparse import ArgumentParser
from core.genericdonwloader import GenericDownloader
from getpass import getpass

KO_CODE = 1
OK_CODE = 0

def main():

    # Setup argument parser
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--comic", dest="comic", action="store",
        help="nom du commic a telecharger")

    # Process arguments
    args = parser.parse_args()
    comic_name = args.comic

    # Launch downloader
    downloader = GenericDownloader(comic_name)
    downloader.downloadComic()

    return OK_CODE

if __name__ == "__main__":
    sys.exit(main())
