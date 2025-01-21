from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
from file_manager import FileManager
from database_manager import DatabaseManager
from ai_manager import AIManager
from file_observer import FileObserverThread

class FileManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OptiGuardiumAI")

        self.file_manager = FileManager()
        self.db_manager = DatabaseManager()
        self.ai_manager = AIManager()

        # Directory to watch
        self.watch_path = "C:\\Users\\Musab\\Desktop"  # Adjust to your own path

        # Start file observer thread
        self.file_observer_thread = FileObserverThread(self.watch_path, self.db_manager)
        self.file_observer_thread.start()

        self.create_widgets()

        # Update recommendations periodically
        self.update_recommendations()

    def create_widgets(self):
        # File operation buttons
        self.create_file_button = ttk.Button(self.root, text="Create File", command=self.create_file)
        self.create_file_button.pack(pady=5)

        self.delete_file_button = ttk.Button(self.root, text="Delete File", command=self.delete_file)
        self.delete_file_button.pack(pady=5)

        # Recommendations list
        self.recommendations_label = ttk.Label(self.root, text="Recommended Files:")
        self.recommendations_label.pack(pady=5)

        self.recommendations_listbox = tk.Listbox(self.root, width=50, height=10)
        self.recommendations_listbox.pack(pady=5)

        self.recommendations_listbox.bind("<Double-Button-1>", self.open_recommended_file)

    def create_file(self):
        """
        Prompt user to select a directory and enter a file name to create a new file.
        """
        path = filedialog.askdirectory()
        if path:
            filename = simpledialog.askstring("Input", "Enter file name:")
            if filename:
                self.file_manager.create_file(path, filename)

    def delete_file(self):
        """
        Prompt user to select a file to delete.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_manager.delete_file(file_path)
            # Delete file from database registry
            self.db_manager.delete_usage(file_path)

    def update_recommendations(self):
        """
        Update the list of recommended files in the GUI.
        """
        # Get current time
        current_time = datetime.now()

        # Get usage history
        usage_history = self.db_manager.get_usage_history()
        print(f"Usage History: {usage_history}")

        # Train the model
        self.ai_manager.train_model(usage_history)

        # Get recommendations from AI manager
        recommendations = self.ai_manager.recommend_files(current_time)
        print(f"Recommendations: {recommendations}")

        # Clear the listbox
        self.recommendations_listbox.delete(0, tk.END)

        # Clear the listbox
        if not recommendations:
            self.recommendations_listbox.insert(tk.END, "No recommendations available.")
        
        else:
            # Insert new recommendations
            for file in recommendations:
                self.recommendations_listbox.insert(tk.END, file)

        # Schedule the next update in 10 seconds
        self.root.after(10000, self.update_recommendations)

    def open_recommended_file(self, event):
        selection = self.recommendations_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.recommendations_listbox.get(index)
            # Open file with default application
            try:
                os.startfile(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {e}")

    def on_close(self):
        """
        Actions to perform when the application is closing.
        """
        self.db_manager.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerGUI(root)
    # Call on_close when the window is closed
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()