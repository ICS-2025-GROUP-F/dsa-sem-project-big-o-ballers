import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from queue import Queue, Task


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue()
        t1 = Task(1, "Test 1", 3)
        q.enqueue(t1)
        self.assertFalse(q.is_empty())
        self.assertEqual(q.dequeue(), t1)

if __name__ == '__main__':
    unittest.main()
