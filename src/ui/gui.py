print("GUI layout initialized")

import tkinter as tk
from tkinter import ttk

class TaskManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Task Manager")
        self.root.geometry("600x400")
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="To-Do Task Manager", font=("Arial", 16))
        title.pack(pady=10)


        # Entry frame
        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(pady=5)

        self.task_entry = ttk.Entry(entry_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT)

        # Task List
        self.tree = ttk.Treeview(self.root, columns=("Task"), show='headings', height=10)
        self.tree.heading("Task", text="Task Description")
        self.tree.column("Task", anchor=tk.W, width=500)
        self.tree.pack(pady=10)

        # Delete button
        delete_button = ttk.Button(self.root, text="Delete Selected", command=self.delete_task)
        delete_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tree.insert("", tk.END, values=(task,))
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

# Only run GUI if this is the main file
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerUI(root)
    root.mainloop()
