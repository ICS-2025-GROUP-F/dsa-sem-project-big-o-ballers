import sqlite3
#db handler
class TaskDatabase:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER,
            status TEXT CHECK(status IN ('To Do', 'In Progress', 'Done')) DEFAULT 'To Do',
            due_date TEXT,
            created_time TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        self.conn.commit()

    def add_task(self, task):
        """task = dict with title, desc, etc."""
        self.conn.execute("""
        INSERT INTO tasks (title, description, priority, status, due_date)
        VALUES (?, ?, ?, ?, ?)
        """, (task['title'], task['description'], task['priority'], task['status'], task['due_date']))
        self.conn.commit()

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return cursor.fetchall()

    def get_task_by_id(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone()

    def update_task(self, task_id, updated_data):
        self.conn.execute("""
        UPDATE tasks
        SET title = ?, description = ?, priority = ?, status = ?, due_date = ?
        WHERE id = ?
        """, (
            updated_data['title'],
            updated_data['description'],
            updated_data['priority'],
            updated_data['status'],
            updated_data['due_date'],
            task_id
        ))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()