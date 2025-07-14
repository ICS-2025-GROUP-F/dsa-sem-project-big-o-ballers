import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_structures.Stack import Stack, TaskAction, UndoRedoManager, TaskHistoryLogger
from data_structures.LinkedList import LinkedList, TaskLinkedList
from datetime import datetime, timedelta


class TestStack(unittest.TestCase):
    """Unit tests for Stack implementation"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.stack = Stack()
        self.limited_stack = Stack(max_size=3)
    
    def test_initialization(self):
        """Test stack initialization"""
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertFalse(self.stack.is_full())
    
    def test_push_and_pop(self):
        """Test basic push and pop operations"""
        # Test push
        self.assertTrue(self.stack.push("item1"))
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 1)
        
        # Test multiple pushes
        self.stack.push("item2")
        self.stack.push("item3")
        self.assertEqual(self.stack.size(), 3)
        
        # Test pop
        item = self.stack.pop()
        self.assertEqual(item, "item3")  # LIFO behavior
        self.assertEqual(self.stack.size(), 2)
        
        # Test pop until empty
        self.stack.pop()
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())
        self.assertIsNone(self.stack.pop())  # Pop from empty stack
    
    def test_peek(self):
        """Test peek operation"""
        self.assertIsNone(self.stack.peek())  # Peek empty stack
        
        self.stack.push("item1")
        self.stack.push("item2")
        
        self.assertEqual(self.stack.peek(), "item2")
        self.assertEqual(self.stack.size(), 2)  # Size unchanged after peek
    
    def test_max_size_constraint(self):
        """Test stack with maximum size constraint"""
        # Fill the limited stack
        for i in range(3):
            self.assertTrue(self.limited_stack.push(f"item{i}"))
        
        self.assertTrue(self.limited_stack.is_full())
        
        # Push to full stack should remove oldest item
        self.limited_stack.push("item3")
        self.assertEqual(self.limited_stack.size(), 3)
        
        # Check that oldest item was removed
        items = self.limited_stack.get_all_items()
        self.assertNotIn("item0", [str(item) for item in items])
    
    def test_search(self):
        """Test search functionality"""
        items = ["item1", "item2", "item3", "item2"]
        for item in items:
            self.stack.push(item)
        
        # Search for existing items
        self.assertEqual(self.stack.search("item2"), 0)  # Top item
        self.assertEqual(self.stack.search("item3"), 1)  # Second from top
        self.assertEqual(self.stack.search("item1"), 3)  # Bottom item
        
        # Search for non-existing item
        self.assertEqual(self.stack.search("nonexistent"), -1)
    
    def test_clear(self):
        """Test clear operation"""
        self.stack.push("item1")
        self.stack.push("item2")
        
        self.stack.clear()
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
    
    def test_get_recent_items(self):
        """Test getting recent items"""
        items = ["item1", "item2", "item3", "item4"]
        for item in items:
            self.stack.push(item)
        
        recent = self.stack.get_recent_items(2)
        self.assertEqual(recent, ["item3", "item4"])
        
        # Test with count larger than stack size
        recent = self.stack.get_recent_items(10)
        self.assertEqual(len(recent), 4)
    
    def test_operation_count(self):
        """Test operation count tracking"""
        initial_count = self.stack.get_operation_count()
        
        self.stack.push("item1")
        self.stack.push("item2")
        self.stack.pop()
        self.stack.clear()
        
        self.assertGreater(self.stack.get_operation_count(), initial_count)


class TestTaskAction(unittest.TestCase):
    """Unit tests for TaskAction class"""
    
    def test_task_action_creation(self):
        """Test TaskAction creation and string representation"""
        task_data = {"id": 1, "title": "Test Task", "status": "todo"}
        action = TaskAction("CREATE", task_data)
        
        self.assertEqual(action.action_type, "CREATE")
        self.assertEqual(action.task_data, task_data)
        self.assertIsNone(action.previous_data)
        self.assertIsNotNone(action.timestamp)
        
        # Test string representation
        str_repr = str(action)
        self.assertIn("CREATE", str_repr)
        self.assertIn("Test Task", str_repr)


class TestUndoRedoManager(unittest.TestCase):
    """Unit tests for UndoRedoManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = UndoRedoManager()
    
    def test_execute_action(self):
        """Test action execution"""
        task_data = {"id": 1, "title": "Test Task"}
        action = TaskAction("CREATE", task_data)
        
        self.manager.execute_action(action)
        
        self.assertTrue(self.manager.can_undo())
        self.assertFalse(self.manager.can_redo())
    
    def test_undo_redo_cycle(self):
        """Test complete undo/redo cycle"""
        task_data = {"id": 1, "title": "Test Task"}
        action = TaskAction("CREATE", task_data)
        
        # Execute action
        self.manager.execute_action(action)
        
        # Undo
        undone_action = self.manager.undo()
        self.assertEqual(undone_action.action_type, "CREATE")
        self.assertFalse(self.manager.can_undo())
        self.assertTrue(self.manager.can_redo())
        
        # Redo
        redone_action = self.manager.redo()
        self.assertEqual(redone_action.action_type, "CREATE")
        self.assertTrue(self.manager.can_undo())
        self.assertFalse(self.manager.can_redo())
    
    def test_clear_redo_on_new_action(self):
        """Test that redo stack is cleared when new action is executed"""
        action1 = TaskAction("CREATE", {"id": 1, "title": "Task 1"})
        action2 = TaskAction("CREATE", {"id": 2, "title": "Task 2"})
        
        self.manager.execute_action(action1)
        self.manager.undo()
        self.assertTrue(self.manager.can_redo())
        
        # Execute new action - should clear redo stack
        self.manager.execute_action(action2)
        self.assertFalse(self.manager.can_redo())
    
    def test_history_summary(self):
        """Test history summary functionality"""
        summary = self.manager.get_history_summary()
        
        self.assertIn('can_undo', summary)
        self.assertIn('can_redo', summary)
        self.assertIn('undo_count', summary)
        self.assertIn('redo_count', summary)
        self.assertIn('recent_actions', summary)


class TestLinkedList(unittest.TestCase):
    """Unit tests for LinkedList implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.linked_list = LinkedList()
    
    def test_initialization(self):
        """Test linked list initialization"""
        self.assertTrue(self.linked_list.is_empty())
        self.assertEqual(self.linked_list.get_size(), 0)
        self.assertIsNone(self.linked_list.head)
        self.assertIsNone(self.linked_list.tail)
    
    def test_insert_at_head(self):
        """Test insertion at head"""
        self.linked_list.insert_at_head("item1")
        self.assertFalse(self.linked_list.is_empty())
        self.assertEqual(self.linked_list.get_size(), 1)
        self.assertEqual(self.linked_list.head.data, "item1")
        self.assertEqual(self.linked_list.tail.data, "item1")
        
        # Insert another item
        self.linked_list.insert_at_head("item2")
        self.assertEqual(self.linked_list.get_size(), 2)
        self.assertEqual(self.linked_list.head.data, "item2")
        self.assertEqual(self.linked_list.tail.data, "item1")
    
    def test_insert_at_tail(self):
        """Test insertion at tail"""
        self.linked_list.insert_at_tail("item1")
        self.assertEqual(self.linked_list.head.data, "item1")
        self.assertEqual(self.linked_list.tail.data, "item1")
        
        self.linked_list.insert_at_tail("item2")
        self.assertEqual(self.linked_list.head.data, "item1")
        self.assertEqual(self.linked_list.tail.data, "item2")
    
    def test_insert_at_position(self):
        """Test insertion at specific position"""
        # Insert in empty list
        self.assertTrue(self.linked_list.insert_at_position(0, "item1"))
        
        # Insert at head
        self.assertTrue(self.linked_list.insert_at_position(0, "item0"))
        
        # Insert at tail
        self.assertTrue(self.linked_list.insert_at_position(2, "item2"))
        
        # Insert in middle
        self.assertTrue(self.linked_list.insert_at_position(2, "item1.5"))
        
        # Test invalid positions
        self.assertFalse(self.linked_list.insert_at_position(-1, "invalid"))
        self.assertFalse(self.linked_list.insert_at_position(10, "invalid"))
    
    def test_delete_operations(self):
        """Test various delete operations"""
        # Setup list with items
        items = ["item1", "item2", "item3"]
        for item in items:
            self.linked_list.insert_at_tail(item)
        
        # Delete at head
        deleted = self.linked_list.delete_at_head()
        self.assertEqual(deleted, "item1")
        self.assertEqual(self.linked_list.get_size(), 2)
        
        # Delete at tail
        deleted = self.linked_list.delete_at_tail()
        self.assertEqual(deleted, "item3")
        self.assertEqual(self.linked_list.get_size(), 1)
        
        # Delete by value
        self.assertTrue(self.linked_list.delete_by_value("item2"))
        self.assertTrue(self.linked_list.is_empty())
        
        # Delete from empty list
        self.assertIsNone(self.linked_list.delete_at_head())
        self.assertFalse(self.linked_list.delete_by_value("nonexistent"))
    
    def test_search_and_access(self):
        """Test search and access operations"""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.linked_list.insert_at_tail(item)
        
        # Test search
        self.assertEqual(self.linked_list.search("item1"), 0)
        self.assertEqual(self.linked_list.search("item2"), 1)
        self.assertEqual(self.linked_list.search("item3"), 2)
        self.assertEqual(self.linked_list.search("nonexistent"), -1)
        
        # Test get_at_index
        self.assertEqual(self.linked_list.get_at_index(0), "item1")
        self.assertEqual(self.linked_list.get_at_index(1), "item2")
        self.assertEqual(self.linked_list.get_at_index(2), "item3")
        self.assertIsNone(self.linked_list.get_at_index(-1))
        self.assertIsNone(self.linked_list.get_at_index(10))
    
    def test_update_and_conversion(self):
        """Test update and conversion operations"""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.linked_list.insert_at_tail(item)
        
        # Test update
        self.assertTrue(self.linked_list.update_at_index(1, "updated_item"))
        self.assertEqual(self.linked_list.get_at_index(1), "updated_item")
        self.assertFalse(self.linked_list.update_at_index(10, "invalid"))
        
        # Test to_list conversion
        result_list = self.linked_list.to_list()
        expected = ["item1", "updated_item", "item3"]
        self.assertEqual(result_list, expected)
    
    def test_reverse(self):
        """Test list reversal"""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.linked_list.insert_at_tail(item)
        
        self.linked_list.reverse()
        
        result_list = self.linked_list.to_list()
        expected = ["item3", "item2", "item1"]
        self.assertEqual(result_list, expected)
    
    def test_iterator(self):
        """Test iterator functionality"""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.linked_list.insert_at_tail(item)
        
        result = []
        for item in self.linked_list:
            result.append(item)
        
        self.assertEqual(result, items)


class TestTaskLinkedList(unittest.TestCase):
    """Unit tests for TaskLinkedList (specialized for tasks)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.task_list = TaskLinkedList()
        self.sample_tasks = [
            {"id": 1, "title": "Task 1", "priority": 2, "status": "todo", "due_date": "2024-12-31"},
            {"id": 2, "title": "Task 2", "priority": 5, "status": "in_progress", "due_date": "2024-12-15"},
            {"id": 3, "title": "Task 3", "priority": 1, "status": "completed", "due_date": "2024-12-01"}
        ]
    
    def test_insert_by_priority(self):
        """Test insertion by priority order"""
        for task in self.sample_tasks:
            self.task_list.insert_task_by_priority(task)
        
        # Should be ordered by priority (high to low)
        tasks = self.task_list.to_list()
        priorities = [task["priority"] for task in tasks]
        self.assertEqual(priorities, [5, 2, 1])
    
    def test_insert_by_due_date(self):
        """Test insertion by due date order"""
        for task in self.sample_tasks:
            self.task_list.insert_task_by_due_date(task)
        
        # Should be ordered by due date (earliest first)
        tasks = self.task_list.to_list()
        due_dates = [task["due_date"] for task in tasks]
        self.assertEqual(due_dates, ["2024-12-01", "2024-12-15", "2024-12-31"])
    
    def test_get_tasks_by_status(self):
        """Test filtering tasks by status"""
        for task in self.sample_tasks:
            self.task_list.insert_at_tail(task)
        
        todo_tasks = self.task_list.get_tasks_by_status("todo")
        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0]["id"], 1)
        
        completed_tasks = self.task_list.get_tasks_by_status("completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0]["id"], 3)
    
    def test_get_high_priority_tasks(self):
        """Test getting high priority tasks"""
        for task in self.sample_tasks:
            self.task_list.insert_at_tail(task)
        
        high_priority = self.task_list.get_high_priority_tasks(min_priority=3)
        self.assertEqual(len(high_priority), 1)
        self.assertEqual(high_priority[0]["id"], 2)
    
    def test_task_operations(self):
        """Test task-specific operations"""
        for task in self.sample_tasks:
            self.task_list.insert_at_tail(task)
        
        # Test mark complete
        self.assertTrue(self.task_list.mark_task_complete(1))
        updated_task = self.task_list.get_task_by_id(1)
        self.assertEqual(updated_task["status"], "completed")
        
        # Test update task
        updates = {"title": "Updated Task", "priority": 4}
        self.assertTrue(self.task_list.update_task(2, updates))
        updated_task = self.task_list.get_task_by_id(2)
        self.assertEqual(updated_task["title"], "Updated Task")
        self.assertEqual(updated_task["priority"], 4)
        
        # Test delete task
        deleted_task = self.task_list.delete_task_by_id(3)
        self.assertIsNotNone(deleted_task)
        self.assertEqual(deleted_task["id"], 3)
        self.assertIsNone(self.task_list.get_task_by_id(3))
    
    def test_get_tasks_summary(self):
        """Test tasks summary generation"""
        for task in self.sample_tasks:
            self.task_list.insert_at_tail(task)
        
        summary = self.task_list.get_tasks_summary()
        
        self.assertEqual(summary["total_tasks"], 3)
        self.assertEqual(summary["completed"], 1)
        self.assertEqual(summary["in_progress"], 1)
        self.assertEqual(summary["todo"], 1)
        self.assertIsInstance(summary["by_category"], dict)


class TestTaskHistoryLogger(unittest.TestCase):
    """Unit tests for TaskHistoryLogger"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.logger = TaskHistoryLogger()
    
    def test_log_operation(self):
        """Test logging operations"""
        self.logger.log_operation("CREATE_TASK", task_id=1, details="Created new task")
        
        logs = self.logger.get_recent_logs(1)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["operation"], "CREATE_TASK")
        self.assertEqual(logs[0]["task_id"], 1)
    
    def test_get_logs_by_task(self):
        """Test getting logs for specific task"""
        self.logger.log_operation("CREATE_TASK", task_id=1, details="Created")
        self.logger.log_operation("UPDATE_TASK", task_id=1, details="Updated")
        self.logger.log_operation("CREATE_TASK", task_id=2, details="Created")
        
        task_1_logs = self.logger.get_logs_by_task(1)
        self.assertEqual(len(task_1_logs), 2)
        
        task_2_logs = self.logger.get_logs_by_task(2)
        self.assertEqual(len(task_2_logs), 1)
    
    def test_export_logs(self):
        """Test log export functionality"""
        self.logger.log_operation("CREATE_TASK", task_id=1, details="Test operation")
        
        exported = self.logger.export_logs()
        self.assertIsInstance(exported, str)
        self.assertIn("CREATE_TASK", exported)
        self.assertIn("Session Log", exported)


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestStack,
        TestTaskAction,
        TestUndoRedoManager,
        TestLinkedList,
        TestTaskLinkedList,
        TestTaskHistoryLogger
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TESTS SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")