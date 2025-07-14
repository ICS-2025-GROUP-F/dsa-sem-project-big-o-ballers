

from datetime import datetime


class TaskAction:
    """Represents an action that can be undone/redone in the Task Manager"""

    def __init__(self, action_type, task_data, previous_data=None):
        """
        Initialize a task action

        Args:
            action_type (str): Type of action ('CREATE', 'UPDATE', 'DELETE')
            task_data (dict): Current task data
            previous_data (dict): Previous task data (for UPDATE operations)
        """
        self.action_type = action_type
        self.task_data = task_data
        self.previous_data = previous_data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        title = self.task_data.get('title', 'Unknown Task') if self.task_data else 'Unknown Task'
        return f"{self.action_type}: {title} at {self.timestamp}"


class Stack:
    """
    Stack implementation for Task Manager

    Used for:
    - Undo/Redo operations
    - Task history tracking
    - Recent actions log

    Time Complexities:
    - Push: O(1)
    - Pop: O(1)
    - Peek: O(1)
    - Search: O(n)
    - Size: O(1)

    Space Complexity: O(n) where n is number of elements
    """

    def __init__(self, max_size=100):
        """
        Initialize stack with optional maximum size

        Args:
            max_size (int): Maximum number of items in stack
        """
        self._items = []
        self._max_size = max_size
        self._operation_count = 0

    def push(self, item):
        """
        Add item to top of stack

        Args:
            item: Item to add to stack

        Returns:
            bool: True if successful, False if stack is full
        """
        if len(self._items) >= self._max_size:
            # Remove oldest item if stack is full (maintain max size)
            self._items.pop(0)

        self._items.append(item)
        self._operation_count += 1
        return True

    def pop(self):
        """
        Remove and return top item from stack

        Returns:
            Item from top of stack or None if empty
        """
        if self.is_empty():
            return None

        self._operation_count += 1
        return self._items.pop()

    def peek(self):
        """
        Return top item without removing it

        Returns:
            Top item or None if empty
        """
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        """Check if stack is empty"""
        return len(self._items) == 0

    def is_full(self):
        """Check if stack is at maximum capacity"""
        return len(self._items) >= self._max_size

    def size(self):
        """Return current number of items in stack"""
        return len(self._items)

    def clear(self):
        """Remove all items from stack"""
        self._items.clear()
        self._operation_count += 1

    def search(self, item):
        """
        Search for item in stack (from top to bottom)

        Args:
            item: Item to search for

        Returns:
            int: Position from top (0 = top) or -1 if not found
        """
        try:
            # Search from top to bottom
            for i in range(len(self._items) - 1, -1, -1):
                if self._items[i] == item:
                    return len(self._items) - 1 - i
            return -1
        except:
            return -1

    def get_all_items(self):
        """
        Return all items in stack (top to bottom order)

        Returns:
            list: Copy of all items from top to bottom
        """
        return list(reversed(self._items))

    def get_recent_items(self, count=5):
        """
        Get most recent items from stack

        Args:
            count (int): Number of recent items to return

        Returns:
            list: Most recent items
        """
        if count <= 0:
            return []

        return self._items[-count:]

    def get_operation_count(self):
        """Return total number of operations performed"""
        return self._operation_count

    def __str__(self):
        """String representation of stack"""
        if self.is_empty():
            return "Stack: [] (empty)"

        items_str = " -> ".join(str(item) for item in reversed(self._items))
        return f"Stack: [{items_str}] (size: {self.size()})"

    def __len__(self):
        """Return size of stack"""
        return len(self._items)


class UndoRedoManager:
    """
    Manages undo/redo operations using two stacks
    Core component for Task Manager operation history
    """

    def __init__(self, max_history=50):
        """
        Initialize undo/redo manager

        Args:
            max_history (int): Maximum number of operations to remember
        """
        self.undo_stack = Stack(max_history)
        self.redo_stack = Stack(max_history)
        self.max_history = max_history

    def execute_action(self, action):
        """
        Execute an action and add to undo history

        Args:
            action (TaskAction): Action that was performed
        """
        # Add to undo stack
        self.undo_stack.push(action)

        # Clear redo stack when new action is performed
        # (can't redo after performing new action)
        self.redo_stack.clear()

    def undo(self):
        """
        Undo last action

        Returns:
            TaskAction: Action that was undone, or None if nothing to undo
        """
        if self.undo_stack.is_empty():
            return None

        action = self.undo_stack.pop()
        self.redo_stack.push(action)
        return action

    def redo(self):
        """
        Redo last undone action

        Returns:
            TaskAction: Action that was redone, or None if nothing to redo
        """
        if self.redo_stack.is_empty():
            return None

        action = self.redo_stack.pop()
        self.undo_stack.push(action)
        return action

    def can_undo(self):
        """Check if undo operation is possible"""
        return not self.undo_stack.is_empty()

    def can_redo(self):
        """Check if redo operation is possible"""
        return not self.redo_stack.is_empty()

    def get_undo_history(self, count=10):
        """
        Get list of actions that can be undone

        Args:
            count (int): Maximum number of actions to return

        Returns:
            list: Recent actions that can be undone
        """
        return self.undo_stack.get_recent_items(count)

    def get_redo_history(self, count=10):
        """
        Get list of actions that can be redone

        Args:
            count (int): Maximum number of actions to return

        Returns:
            list: Actions that can be redone
        """
        return self.redo_stack.get_recent_items(count)

    def clear_history(self):
        """Clear all undo/redo history"""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history_summary(self):
        """
        Get summary of current undo/redo state

        Returns:
            dict: Summary with undo/redo counts and recent actions
        """
        return {
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo(),
            'undo_count': self.undo_stack.size(),
            'redo_count': self.redo_stack.size(),
            'recent_actions': [str(action) for action in self.get_undo_history(5)]
        }


class TaskHistoryLogger:
    """
    Specialized stack for logging task operations
    Used for debugging and monitoring task manager operations
    """

    def __init__(self, max_logs=200):
        """
        Initialize task history logger

        Args:
            max_logs (int): Maximum number of log entries to keep
        """
        self.log_stack = Stack(max_logs)
        self.session_start = datetime.now()

    def log_operation(self, operation_type, task_id=None, details=None):
        """
        Log a task operation

        Args:
            operation_type (str): Type of operation performed
            task_id (int): ID of task involved (if applicable)
            details (str): Additional details about the operation
        """
        log_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'operation': operation_type,
            'task_id': task_id,
            'details': details or '',
            'session_time': (datetime.now() - self.session_start).total_seconds()
        }

        self.log_stack.push(log_entry)

    def get_recent_logs(self, count=20):
        """
        Get recent log entries

        Args:
            count (int): Number of recent logs to return

        Returns:
            list: Recent log entries
        """
        return self.log_stack.get_recent_items(count)

    def get_logs_by_task(self, task_id):
        """
        Get all logs related to a specific task

        Args:
            task_id (int): Task ID to filter by

        Returns:
            list: Log entries for the specified task
        """
        all_logs = self.log_stack.get_all_items()
        return [log for log in all_logs if log.get('task_id') == task_id]

    def clear_logs(self):
        """Clear all log entries"""
        self.log_stack.clear()

    def export_logs(self):
        """
        Export logs in a readable format

        Returns:
            str: Formatted log output
        """
        logs = self.get_recent_logs(50)  # Get last 50 logs

        if not logs:
            return "No logs available"

        output = f"=== Task Manager Session Log ===\n"
        output += f"Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"Total operations logged: {self.log_stack.size()}\n\n"

        for log in reversed(logs):  # Show most recent first
            output += f"[{log['timestamp']}] {log['operation']}"
            if log['task_id']:
                output += f" (Task ID: {log['task_id']})"
            if log['details']:
                output += f" - {log['details']}"
            output += "\n"

        return output


# Example usage and testing functions
def test_stack_operations():
    """Test basic stack operations"""
    print("=== Testing Stack Operations ===")

    stack = Stack(5)

    # Test push operations
    items = ["Task 1", "Task 2", "Task 3"]
    for item in items:
        stack.push(item)
        print(f"Pushed: {item}, Stack size: {stack.size()}")

    print(f"Stack contents: {stack}")
    print(f"Top item: {stack.peek()}")

    # Test pop operations
    while not stack.is_empty():
        item = stack.pop()
        print(f"Popped: {item}, Remaining size: {stack.size()}")

    print(f"Final stack: {stack}")


def test_undo_redo_manager():
    """Test undo/redo functionality"""
    print("\n=== Testing Undo/Redo Manager ===")

    manager = UndoRedoManager()

    # Simulate task operations
    tasks = [
        {"id": 1, "title": "Complete project proposal", "status": "todo"},
        {"id": 2, "title": "Review team code", "status": "in_progress"},
        {"id": 3, "title": "Update documentation", "status": "done"}
    ]

    # Execute some actions
    for task in tasks:
        action = TaskAction("CREATE", task)
        manager.execute_action(action)
        print(f"Executed: {action}")

    print(f"\nUndo available: {manager.can_undo()}")
    print(f"Redo available: {manager.can_redo()}")

    # Test undo
    undone = manager.undo()
    print(f"Undone: {undone}")
    print(f"Can redo now: {manager.can_redo()}")

    # Test redo
    redone = manager.redo()
    print(f"Redone: {redone}")

    # Show history summary
    summary = manager.get_history_summary()
    print(f"History summary: {summary}")


def test_task_history_logger():
    """Test task history logging"""
    print("\n=== Testing Task History Logger ===")

    logger = TaskHistoryLogger()

    # Log some operations
    logger.log_operation("CREATE_TASK", 1, "Created new task")
    logger.log_operation("UPDATE_TASK", 1, "Updated task status")
    logger.log_operation("DELETE_TASK", 2, "Deleted completed task")

    # Get recent logs
    recent_logs = logger.get_recent_logs(5)
    print(f"Recent logs: {len(recent_logs)} entries")

    # Export logs
    log_output = logger.export_logs()
    print("Exported logs:")
    print(log_output)


if __name__ == "__main__":
    # Run all tests
    test_stack_operations()
    test_undo_redo_manager()
    test_task_history_logger()