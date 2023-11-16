import os
import hashlib
from pathlib import Path
import logging


class FileDuplicateRemover:
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self.logger = self._setup_logger()
        self._remove_duplicates()

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger("FileDuplicateRemover")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger

    @staticmethod
    def calculate_hash(file_path: Path) -> str:
        try:
            with file_path.open("rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logging.error(f"Error calculating hash for {file_path}: {e}")
            return ""

    def _remove_duplicates(self) -> None:
        unique_hashes = set()
        count = 0

        try:
            for file_path in self.directory_path.iterdir():
                if file_path.is_file():
                    file_hash = self.calculate_hash(file_path)

                    if not file_hash:
                        continue

                    if file_hash not in unique_hashes:
                        unique_hashes.add(file_hash)
                    else:
                        self.logger.info(f"Deleting duplicate file: {file_path}")
                        file_path.unlink()
                        count += 1

            self.logger.info(
                f"{count} non-unique files removed from {self.directory_path}"
            )

        except Exception as e:
            self.logger.error(f"Error during duplicate removal: {e}")


if __name__ == "__main__":
    target_directory = "/mnt/d/downloads/mem_tv13gachi"
    duplicate_remover = FileDuplicateRemover(target_directory)
