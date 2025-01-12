import os
import shutil


class FileManager:
    def __init__(self):
        pass
    def create_file(path, name):
        full_path = os.path.join(path, name)
        with open(full_path, 'w') as file:
            file.write("")
        print(f"{full_path} created successfully.")

    def delete_file(path):
        if os.path.isfile(path):
            os.remove(path)
            print(f"{path} deleted successfully.")
        else:
            print(f"{path} does not exist.")

    def list_files(path):
        try:
            for element in os.listdir(path):
                print(element)
        except Exception as e:
            print(f"Error: {str(e)}")