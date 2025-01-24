import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog, messagebox

class FileManagerGUI(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("OptiGuardiumAI")
        
        self.apply_styles()

        self.create_widgets()

        self.create_menu()

        self.bind_shortcuts()

        # Update recommendations periodically
        self.update_recommendations()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TLabelFrame", font=("Arial", 10, "bold"))

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File operation frame
        file_ops_frame = ttk.LabelFrame(main_frame, text="File Operations")
        file_ops_frame.pack(fill=tk.X, pady=5)

        # File operation buttons
        self.create_file_button = ttk.Button(file_ops_frame, text="Create File", command=self.create_file)
        self.create_file_button.pack(pady=5)

        self.delete_file_button = ttk.Button(file_ops_frame, text="Delete File", command=self.delete_file)
        self.delete_file_button.pack(pady=5)

        # Recommendations list
        recommendations_frame = ttk.LabelFrame(main_frame, text="Recommended Files")
        recommendations_frame.pack(fill=tk.BOTH, expand=True,pady=5)

        self.recommendations_listbox = tk.Listbox(recommendations_frame)
        self.recommendations_listbox.pack(fill=tk.BOTH, expand=True, padx=5,pady=5)
        self.recommendations_listbox.bind("<Double-Button-1>", self.open_recommended_file)

    def create_menu(self):
        menubar = tk.Menu(self)
        self.configure(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Create File", command=self.create_file)
        file_menu.add_command(label="Delete File", command=self.delete_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_file(self):
        """
        Prompt user to select a directory and enter a file name to create a new file.
        """
        path = filedialog.askdirectory()
        if path:
            filename = simpledialog.askstring("Input", "Enter file name:")
            if filename:
                self.controller.file_manager.create_file(path, filename)

    def delete_file(self):
        """
        Prompt user to select a file to delete.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.controller.file_manager.delete_file(file_path)
            # Delete file from database registry
            self.controller.db_manager.delete_usage(file_path)

    def update_recommendations(self):
        """
        Update the list of recommended files in the GUI.
        """
        # Get current time
        current_time = self.controller.get_current_time()

        # Get usage history
        usage_history = self.controller.db_manager.get_usage_history()
        print(f"Usage History: {usage_history}")

        # Train the model
        self.controller.ai_manager.train_model(usage_history)

        # Get recommendations from AI manager
        recommendations = self.controller.ai_manager.recommend_files(current_time)
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
        self.after(10000, self.update_recommendations)

    def open_recommended_file(self, event):
        selection = self.recommendations_listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.recommendations_listbox.get(index)
            # Open file with default application
            try:
                self.controller.file_manager.open_file(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open file: {e}")

    def on_close(self):
        """
        Actions to perform when the application is closing.
        """
        self.controller.db_manager.close()
        self.destroy()

    def show_about(self):
        messagebox.showinfo("About", "OptiGuardiumAI\nVersion 0.1")

    def bind_shortcuts(self):
        self.bind('<Control-n>', lambda event: self.create_file())
        self.bind('<Control-d>', lambda event: self.delete_file())
        self.bind('<Control-q>', lambda event: self.on_close())

    def run(self):
        self.mainloop()
    