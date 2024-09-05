import os
import hashlib
from pathlib import Path
import logging


class FileDuplicateRemover:
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self.logger = self._setup_logger()

        self.logger.debug(f"Searching {directory_path} for non-unique files ... \n")
        self._remove_duplicates()

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger("FileDuplicateRemover")
        logger.setLevel(logging.debug)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger

    def calculate_hash(self, file_path: Path) -> str:
        self.logger.debug(f"Calculating hash for {file_path} ...")
        hash_obj = hashlib.sha256()
        try:
            with file_path.open("rb") as f:
                while chunk := f.read(8192):
                    hash_obj.update(chunk)
            file_hash = hash_obj.hexdigest()
            self.logger.debug(f"Hash for {file_path}: {file_hash}")
            return file_hash
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def _remove_duplicates(self) -> None:
        unique_hashes = set()
        count = 0

        try:
            for dirpath, _, filenames in os.walk(self.directory_path):
                for filename in filenames:
                    file_path = Path(dirpath) / filename
                    self.logger.debug(f"Processing file: {file_path}")
                    file_hash = self.calculate_hash(file_path)
                    if not file_hash:
                        continue

                    if file_hash not in unique_hashes:
                        unique_hashes.add(file_hash)
                    else:
                        self.logger.debug(f"Deleting duplicate file: {file_path}")
                        file_path.unlink()
                        count += 1

            self.logger.info(
                f"{count} non-unique files removed from {self.directory_path}"
            )

        except Exception as e:
            self.logger.error(f"Error during duplicate removal: {e}")
