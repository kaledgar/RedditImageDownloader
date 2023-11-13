"""
https://gist.github.com/tfeldmann/fc875e6630d11f2256e746f67a09c1ae
Fast duplicate file finder.
Usage: duplicates.py <folder> [<folder>...]
Based on https://stackoverflow.com/a/36113168/300783
Modified for Python3 with some small code improvements.
"""
import os
import sys
import hashlib
from collections import defaultdict

import pathlib
import logging

logger = logging.getLogger(__name__)


class ImageDuplicateRemoval:
    """
    Simple class to remove non unique files in a given directory
    """

    def __init__(self, paths: list, username: str):
        """initialization and execution of the main method

        Args:
            paths (list of str): list of paths to seek duplicates
        """
        self.paths = paths
        self.username = username
        self.duplicate_paths = self.find_duplicates()
        self.duplicate_files_list = self.get_duplicate_files_list()

        self.execute()

    def chunk_reader(self, fobj, chunk_size=1024):
        """Generator that reads a file in chunks of bytes"""
        while True:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def get_hash(self, filename, first_chunk_only=False, hash_algo=hashlib.sha1):
        hashobj = hash_algo()
        with open(filename, "rb") as f:
            if first_chunk_only:
                hashobj.update(f.read(1024))
            else:
                for chunk in self.chunk_reader(f):
                    hashobj.update(chunk)
        return hashobj.digest()

    def find_duplicates(self) -> list:
        files_by_size = defaultdict(list)
        files_by_small_hash = defaultdict(list)
        files_by_full_hash = dict()

        duplicate_list = []

        for path in self.paths:
            for dirpath, _, filenames in os.walk(path):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    try:
                        full_path = os.path.realpath(full_path)
                        file_size = os.path.getsize(full_path)
                    except OSError:
                        continue
                    files_by_size[file_size].append(full_path)
        for file_size, files in files_by_size.items():
            if len(files) < 2:
                continue

            for filename in files:
                try:
                    small_hash = self.get_hash(filename, first_chunk_only=True)
                except OSError:
                    continue
                files_by_small_hash[(file_size, small_hash)].append(filename)
        for files in files_by_small_hash.values():
            if len(files) < 2:
                continue
            for filename in files:
                try:
                    full_hash = self.get_hash(filename, first_chunk_only=False)
                except OSError:
                    continue
                if full_hash in files_by_full_hash:
                    duplicate = files_by_full_hash[full_hash]
                    duplicate_list.append(duplicate)
                else:
                    files_by_full_hash[full_hash] = filename

        return duplicate_list

    def get_duplicate_files_list(self) -> list:
        duplicate_files_list = []
        for path in self.duplicate_paths:
            duplicate_files_list.append(path.split(self.username + "/", 1)[1])
        return duplicate_files_list

    def execute(self):
        if os.getcwd() not in self.paths:
            os.chdir(self.paths[0])
        logger.debug(os.getcwd())
        for file in self.duplicate_files_list:
            pathlib.Path(file).unlink(missing_ok=True)

        logger.info(f"""{len(self.duplicate_files_list)} non-unique files removed""")
