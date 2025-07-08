from taskdb import TaskDatabase

def test_db_creation():
    db = TaskDatabase()
    db.close()
    print("Database initialized.")

test_db_creation()
