# tests/test_db_init.py

from taskdb import TaskDatabase

def test_db_creation():
    db = TaskDatabase()  # This will create tasks.db in project root
    db.close()
    print("Database initialized.")

test_db_creation()
