from pathlib import Path
from flask import current_app

class SpeedFileManager:
    def __init__(self, file_path: Path, mode: str):
        self.file_path: Path = file_path
        self.mode = mode
        self.file = None

    def __enter__(self):
        try:
            self.file = open(self.file_path, mode=self.mode)
            return self
        except FileNotFoundError as e:
            current_app.logger.error(f"File not found: {str(e)}")
        except IOError as e:
            current_app.logger.error(f"File IO error not found:{str(e)}")
        except Exception as e:
            current_app.logger.error(f"File open error: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def write(self, text: str):
        try:
            self.file.write(text)
        except IOError as e:
            current_app.logger.error(f"File write IO error not found:{str(e)}")
        except Exception as e:
            current_app.logger.error(f"File write error: {str(e)}")

    def close(self):
        if self.file is not None:
            try:
                self.file.close()
            except Exception as e:
                current_app.logger.error(f"File close error: {str(e)}")
                exit(-1)
