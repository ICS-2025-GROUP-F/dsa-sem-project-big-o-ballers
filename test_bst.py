import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bst import BST, TaskNode
import unittest

class Task:
    def __init__(self, task_id, title, priority):
        self.task_id = task_id
        self.title = title
        self.priority = priority

    def __repr__(self):
        return f"{self.task_id}: {self.title} ({self.priority})"

    def __eq__(self,other):#checks for equals in the  binary tree
        return(
            isinstance(other,Task) and
            self.task_id == other.task_id and
            self.title == other.title and
            self.priority == other.priority
        )


class TestBST(unittest.TestCase):
    def test_insert_and_search(self):
        bst = BST()
        t1 = Task(1, "Task A", 3)
        t2 = Task(2, "Task B", 5)
        t3 = Task(3,"Task C",2)
        bst.insert(t1)
        bst.insert(t2)
        bst.insert(t3)
        self.assertEqual(bst.search(3), t1)
        self.assertEqual(bst.search(5), t2)
        self.assertEqual(bst.search(2),t3)

if __name__ == '__main__':
    unittest.main()
