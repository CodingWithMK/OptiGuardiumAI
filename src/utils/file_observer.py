import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, db_manager, file_manager):
        super().__init__()
        self.db_manager = db_manager
        self.file_manager = file_manager

    def on_modified(self, event):
        if not event.is_directory:
            print(f"Modified: {event.src_path}")
            self.db_manager.insert_usage(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"Created: {event.src_path}")
            self.db_manager.insert_usage(event.src_path)
            self.file_manager.process_file(event.src_path)  # Process the new file

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"Deleted: {event.src_path}")
            self.db_manager.delete_usage(event.src_path)

class FileObserverThread(threading.Thread):
    def __init__(self, paths, db_manager, file_manager):
        super().__init__()
        self.paths = paths # List of directories to watch
        self.db_manager = db_manager
        self.file_manager = file_manager
        self.observers = []
        self.daemon = True  # Ensure thread exits when main program exits

    def run(self):
        # Scan existing files in directories
        for path in self.paths:
            self.scan_existing_files(path)

        # Start observers for each directory
        for path in self.paths:
            event_handler = FileEventHandler(self.db_manager, self.file_manager)
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            self.observers.append(observer)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()
            for observer in self.observers:
                observer.join()

    def scan_existing_files(self, path):
        """
        Existing files in the directory are scanned and inserted into the database.
        """
        allowed_extensions = [".txt", ".pdf", ".jpg", ".png", ".docx", ".mp3", ".pptx"]
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in allowed_extensions):
                    file_path = os.path.join(root, file)
                    print(f"Existing file added to usage_history: {file_path}")
                    self.db_manager.insert_usage(file_path)
                    self.file_manager.process_file(file_path)