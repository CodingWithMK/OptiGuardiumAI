import os
import time
from watchdog.observers import Observer
from file_observer import FileEventHandler
from database_manager import DatabaseManager
from file_manager import FileManager
from ai_manager import AIManager

def main():
    db_manager = DatabaseManager()
    file_manager = FileManager()
    ai_manager = AIManager()
    path = "C:\\Users\\Musab\\Downloads"

    # Event Handler and Observer
    event_handler = FileEventHandler(db_manager)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            # Use usage history
            usage_history = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
            recommendations = ai_manager.recommend_files(usage_history)
            print("Recommended files: ")
            for file in recommendations:
                print(file)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # Stop Database Connection
    db_manager.close()
    

if __name__ == "__main__":
    main()
    
    
    