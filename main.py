import tkinter as tk
from tkinter import ttk, messagebox
from db.taskdb import TaskDatabase

# Initialize DB
db = TaskDatabase()

# --- GUI Class ---
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager - Big O Ballers 🧠💻")
        self.root.geometry("900x500")

        # Task Form
        form_frame = tk.Frame(root, pady=10)
        form_frame.pack()

        tk.Label(form_frame, text="Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Priority:").grid(row=0, column=2)
        self.priority_spin = tk.Spinbox(form_frame, from_=1, to=5, width=5)
        self.priority_spin.grid(row=0, column=3)

        tk.Label(form_frame, text="Due Date (YYYY-MM-DD):").grid(row=0, column=4)
        self.due_entry = tk.Entry(form_frame)
        self.due_entry.grid(row=0, column=5)

        tk.Button(form_frame, text="Add Task", command=self.add_task).grid(row=0, column=6, padx=10)

        # Task Table
        self.tree = ttk.Treeview(root, columns=("ID", "Title", "Priority", "Status", "Due Date"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(expand=True, fill="both", pady=10)

        # Action Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Mark as Done", command=self.mark_done).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=10)
        tk.Button(button_frame, text="Refresh", command=self.load_tasks).pack(side="left", padx=10)

        self.load_tasks()

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = db.get_all_tasks()

        tasks.sort(key=lambda t: t[3], reverse=True)  # t[3] = priority

        for task in tasks:
            self.tree.insert("", "end", values=(task[0], task[1], task[3], task[4], task[5]))


    def add_task(self):
        title = self.title_entry.get()
        priority = int(self.priority_spin.get())
        due = self.due_entry.get()

        if not title or not due:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        task = {
            'title': title,
            'description': '',
            'priority': priority,
            'status': 'To Do',
            'due_date': due
        }
        db.add_task(task)
        self.load_tasks()
        self.title_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a task to delete.")
            return

        task_id = self.tree.item(selected[0])['values'][0]
        db.delete_task(task_id)
        self.load_tasks()

    def mark_done(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a task to mark done.")
            return

        task_id = self.tree.item(selected[0])['values'][0]
        task = db.get_task_by_id(task_id)

        if task:
            updated_data = {
                'title': task[1],
                'description': task[2],
                'priority': task[3],
                'status': 'Done',
                'due_date': task[5]
            }
            db.update_task(task_id, updated_data)
            self.load_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
