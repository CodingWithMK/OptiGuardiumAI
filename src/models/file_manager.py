import os
import shutil

class FileManager:
    def __init__(self):
        pass

    def open_file(self, file_path):
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def create_file(self, path, name):
        """
        Create a new file at the given path with the specified name.
        """
        full_path = os.path.join(path, name)
        with open(full_path, 'w') as file:
            file.write('')
        print(f"{full_path} has been created.")

    def delete_file(self, path):
        """
        Delete the file at the given path.
        """
        if os.path.isfile(path):
            os.remove(path)
            print(f"{path} has been deleted.")
        else:
            print(f"{path} not found.")

    def list_directory(self, path):
        """
        List all items in the given directory path.
        """
        try:
            items = os.listdir(path)
            for item in items:
                print(item)
        except Exception as e:
            print(f"Error: {e}")