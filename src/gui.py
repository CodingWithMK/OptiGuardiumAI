from tkinter import messagebox, ttk
import tkinter
from tkinter import *
import tkinter.filedialog
import tkinter.simpledialog
import os
from file_manager import FileManager

class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OptiGuardiumAI")
        self.file_manager = FileManager()
        self.create_widgets()

    def create_widgets(self):
        self.create_file_button = ttk.Button(self.root, text="Create File", command=self.create_file)
        self.create_file_button.pack(pady=10)

        self.delete_file_button = ttk.Button(self.root, text="Delete File", command=self.delete_file)
        self.delete_file_button.pack(pady=10)

        self.list_dir_button = ttk.Button(self.root, text="List Files", command=self.list_directory)
        self.list_dir_button.pack(pady=10)

    def create_file(self):
        path = tkinter.filedialog.askdirectory()
        if path:
            filename = tkinter.simpledialog.askstring("Input", "Enter file name: ")
            if filename:
                self.file_manager.create_file(path, filename)

    def delete_file(self):
        file_path = tkinter.filedialog.askopenfilename()
        if file_path:
            self.file_manager.delete_file(file_path)

    def list_directory(self):
        path = tkinter.filedialog.askdirectory()
        if path:
            items = os.listdir(path)
            item_list = "\n".join(items)
            messagebox.showinfo("Directory Contents", item_list)


if __name__ == "__main__":
    root = tkinter.Tk()
    gui = FileManagerGUI(root)
    root.mainloop()