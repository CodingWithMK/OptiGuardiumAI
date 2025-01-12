import os
from file_manager import FileManager
from ai_manager import AIManager

def main():
    file_manager = FileManager()
    ai = AIManager()
    path = "C:\\Users\\Musab\\Downloads"

    # Create a file
    file_manager.create_file(path, "optguard_test.txt")

    # List all files in directory
    file_manager.list_files(path)

    # Delete a file
    file_manager.delete_file(os.path.join(path, "optguard_test.txt"))

    # Recommend files
    # Example files history
    usage_history = [file[:9] for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    recommendations = ai.recommend_files(usage_history)
    print("Recommended files: ")
    for file in recommendations:
        print(file)

if __name__ == "__main__":
    main()
    
    
    