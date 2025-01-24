from models.file_manager import FileManager
from models.database_manager import DatabaseManager
from models.ai_manager import AIManager
from views.gui import FileManagerGUI
from utils.file_observer import FileObserverThread
import threading
from datetime import datetime

class MainController:
    def __init__(self):
        self.file_manager = FileManager()
        self.db_manager = DatabaseManager()
        self.ai_manager = AIManager()
        self.watch_path = "C:\\Users\\Musab\\Desktop"

        # Start file observer thread
        self.file_observer_thread = FileObserverThread(self.watch_path, self.db_manager)
        self.file_observer_thread.start()

    def get_current_time(self):
        return datetime.now()

    def run(self):
        # Start GUI
        self.gui = FileManagerGUI(self)
        self.gui.run()