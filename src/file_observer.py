# src/file_observer.py

import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

    def on_modified(self, event):
        if not event.is_directory:
            print(f"Modified: {event.src_path}")
            self.db_manager.insert_usage(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"Created: {event.src_path}")
            self.db_manager.insert_usage(event.src_path)

class FileObserverThread(threading.Thread):
    def __init__(self, path, db_manager):
        super().__init__()
        self.path = path
        self.db_manager = db_manager
        self.observer = Observer()
        self.daemon = True  # Ensure thread exits when main program exits

    def run(self):
        # Scanning existing files in directory
        self.scan_existing_files()

        event_handler = FileEventHandler(self.db_manager)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def scan_existing_files(self):
        """
        Existing files in the directory arescanned and inserted into the database.
        """
        allowed_extensions = [".pdf", ".docx", ".mp3", ".pptx"]
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if any(file.endswith(ext) for ext in allowed_extensions):
                    file_path = os.path.join(root, file)
                    print(f"Existing file added to usage_history: {file_path}")
                    self.db_manager.insert_usage(file_path)