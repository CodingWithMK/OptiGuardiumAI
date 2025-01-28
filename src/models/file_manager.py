import os
import shutil
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Downloading NLTK resources if not already present
def download_nltk_resources():
    required_resources = [
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
    ]
    for (nltk_path, download_name) in required_resources:

        try:
            nltk.data.find(nltk_path)
            print("NLTK resources already downloaded.")
        except LookupError:
            print("NLTK resources not found. Downloading now...")
            nltk.download(download_name)
            print(f"NLTK resources downloaded succesfully.")
    
download_nltk_resources()

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

    def read_file_content(self, file_path):
        """
        Read the content of the file at the given path.

        Parameters:
            file_path (str): Path to the file.

        Returns:
        str: Content of the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
        
    def extract_keywords(self, text):
        """
        Extract keywords drom the given text using NLP techniques.

        Parameters:
            text (str): Input text.

        Returns:
            list: List of extracted keywords.
        """
        # Tokenize the text into words
        tokens = word_tokenize(text, language='english')

        # Convert all tokens to lowercase and keep only alphabetic tokens
        tokens = [word.lower() for word in tokens if word.isalpha()]

        # Define stop words in Turkish
        english_stop_words = set(stopwords.words('english'))

        # Filter out stop words from tokens
        filtered_tokens = [word for word in tokens if word not in english_stop_words]

        # Calculate the frequency distribution of tokens
        freq_dist = nltk.FreqDist(filtered_tokens)

        # Get the top 3 most common words
        common_words = freq_dist.most_common(3)

        # Extract the keywords
        keywords = [word for word, freq in common_words]

        return keywords
    
    def rename_file_based_on_content(self, file_path):
        """
        Rename the file based on its content by extracting keywords.

        Parameters:
            file_path (str): Path of the file.

        Returns:
            str: New file path after renaming.
        """
        content = self.read_file_content(file_path)
        if content:
            keywords = self.extract_keywords(content)
            if keywords:
                dir_name = os.path.dirname(file_path)
                extension = os.path.splitext(file_path)[1]
                # Create new file name by joining keywords with underscores
                new_name = "_".join(keywords) + extension
                new_path = os.path.join(dir_name, new_name)

                try:
                    os.rename(file_path, new_path)
                    print(f"File renamed to: {new_path}")
                except Exception as e:
                    print(f"Error renaming file: {e}")
        return file_path
    
    def move_file_to_directory(self, file_path, target_directory):
        """
        Move the file to the target directory.

        Parameters:
            file_path (str): Path to the file.
            target_directory (str): Target directory where the file will be moved.

        Returns:
            str: New file path after moving.
        """
        try:
            # Create the target directory if it does not exist
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
            file_name = os.path.basename(file_path)
            new_path = os.path.join(target_directory, file_name)
            shutil.move(file_path, new_path)
            print(f"File moved to: {new_path}")
            return new_path
        except Exception as e:
            print(f"Error moving file: {e}")
            return file_path
        
    def process_file(self, file_path):
        """
        Process the file: Rename based on content and move to appropriate directory.

        Parameters:
            file_path (str): Path to the file.
        
        Returns:
            str: Final file path after processing.
        """
        # Rename the file based on its content
        new_file_path = self.rename_file_based_on_content(file_path)

        # Determine the extension of the file
        _, extension = os.path.splitext(new_file_path)
        extension = extension.lower()

        # Define target directories based on file extension
        extension_to_directory = {
            '.txt': 'C:\\Users\\Musab\\Downloads\\TextFiles',
            '.pdf': 'C:\\Users\\Musab\\Downloads\\PDFs',
            '.jpeg': 'C:\\Users\\Musab\\Downloads\\Images',
            '.jpg': 'C:\\Users\\Musab\\Downloads\\Images',
            '.png': 'C:\\Users\\Musab\\Downloads\\Images',
        }

        target_directory = extension_to_directory.get(extension)

        if target_directory:
            # Move the file to the target directory
            final_path = self.move_file_to_directory(new_file_path, target_directory)
            return final_path
        else:
            print(f"No target directory defined for extension: {extension}")
            return new_file_path
