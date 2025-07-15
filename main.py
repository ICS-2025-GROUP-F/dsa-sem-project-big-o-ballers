import tkinter as tk
from tkinter import ttk, messagebox
from db.taskdb import TaskDatabase
from data_structures.LinkedList import TaskLinkedList
from data_structures.Stack import UndoRedoManager, TaskAction
from data_structures.queue import Queue
from data_structures.bst import BST
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.db = TaskDatabase()

        # Data Structures
        self.task_list = TaskLinkedList()
        self.task_queue = Queue()
        self.task_bst = BST()
        self.undo_redo = UndoRedoManager()

        self.setup_ui()
        self.load_tasks()
        self.mark_done_button = tk.Button(root, text="Mark as Done", command=self.mark_task_done)
        self.mark_done_button.pack(pady=5)


    def setup_ui(self):
        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Priority", "Status", "Due Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Add Task", command=self.add_task_popup).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Delete", command=self.delete_selected).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Undo", command=self.undo).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Redo", command=self.redo).pack(side=tk.LEFT)
    def mark_task_done(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to mark as done.")
            return

        task_values = self.tree.item(selected, "values")
        task_id = int(task_values[0])

    # Fetch the task and update its status
        task = self.db.get_task_by_id(task_id)
        if task:
            updated_task = {
                'title': task[1],
                'description': task[2] if task[2] else "",
                'priority': task[3],
                'status': "Done",
                'due_date': task[5]
            }
            self.db.update_task(task_id, updated_task)
            self.load_tasks()
            messagebox.showinfo("Success", f"Task '{task[1]}' marked as done.")

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Clear data structures
        self.task_list.clear()
        self.task_queue = Queue()
        self.task_bst = BST()

        tasks = self.db.get_all_tasks()
        for task in tasks:
            task_data = {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'priority': task[3],
                'status': task[4],
                'due_date': task[5]
            }
            self.task_list.insert_task_by_priority(task_data)
            self.task_queue.enqueue(task_data)
            self.task_bst.insert({
                'id': task[0],
                'title': task[1],
                'priority': task[3],
                'status': task[4] if task[4] else 'To Do',
                'due_date': task[5]
            })

           

        for task in self.task_list.to_list():
            self.tree.insert("", "end", values=(task['id'], task['title'], task['priority'], task['status'], task['due_date']))

    def add_task_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Task")

        labels = ["Title", "Description", "Priority", "Status", "Due Date (YYYY-MM-DD)"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(popup, text=label).grid(row=i, column=0)
            entries[label] = tk.Entry(popup)
            entries[label].grid(row=i, column=1)

        def save():
            task = {
                'title': entries["Title"].get(),
                'description': entries["Description"].get(),
                'priority': int(entries["Priority"].get()),
                'status': entries["Status"].get(),
                'due_date': entries["Due Date (YYYY-MM-DD)"].get()
            }
            self.db.add_task(task)
            self.undo_redo.execute_action(TaskAction("CREATE", task))
            popup.destroy()
            self.load_tasks()

        tk.Button(popup, text="Save", command=save).grid(row=len(labels), columnspan=2)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return

        task_id = int(self.tree.item(selected[0])['values'][0])
        task_data = self.db.get_task_by_id(task_id)

        if task_data:
            self.db.delete_task(task_id)
            self.undo_redo.execute_action(TaskAction("DELETE", {
                'id': task_data[0],
                'title': task_data[1],
                'description': task_data[2],
                'priority': task_data[3],
                'status': task_data[4],
                'due_date': task_data[5]
            }))
            self.load_tasks()

    def undo(self):
        action = self.undo_redo.undo()
        if not action:
            messagebox.showinfo("Undo", "No actions to undo.")
            return

        if action.action_type == "CREATE":
            task_id = self.db.get_all_tasks()[-1][0]  # crude way to get last inserted
            self.db.delete_task(task_id)
        elif action.action_type == "DELETE":
            self.db.add_task(action.task_data)
        elif action.action_type == "UPDATE":
            self.db.update_task(action.task_data['id'], action.previous_data)

        self.load_tasks()

    def redo(self):
        action = self.undo_redo.redo()
        if not action:
            messagebox.showinfo("Redo", "No actions to redo.")
            return

        if action.action_type == "CREATE":
            self.db.add_task(action.task_data)
        elif action.action_type == "DELETE":
            self.db.delete_task(action.task_data['id'])
        elif action.action_type == "UPDATE":
            self.db.update_task(action.task_data['id'], action.task_data)

        self.load_tasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
