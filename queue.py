class Task:
    def __init__(self, task_id, title, priority):
        self.task_id = task_id
        self.title = title
        self.priority = priority

    def __repr__(self):
        return f"{self.task_id}: {self.title} ({self.priority})"

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, task):
        self.items.append(task)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def peek(self):
        if not self.is_empty():
            return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        return ' <- '.join([str(item) for item in self.items])
