from datetime import datetime, timedelta


class Node:
    """
    Node class for linked list
    Each node contains task data and reference to next node
    """

    def __init__(self, data):
        """
        Initialize node with data

        Args:
            data: Data to store in node
        """
        self.data = data
        self.next = None

    def __str__(self):
        """String representation of node"""
        if isinstance(self.data, dict) and 'title' in self.data:
            return f"Node({self.data['title']})"
        return f"Node({str(self.data)})"


class LinkedList:
    """
    Singly Linked List implementation for Task Manager

    Used for:
    - Maintaining ordered list of tasks
    - Sequential task processing
    - Task organization and management

    Time Complexities:
    - Insert at head: O(1)
    - Insert at tail: O(1) with tail pointer
    - Insert at position: O(n)
    - Delete at head: O(1)
    - Delete at tail: O(n) without tail pointer optimization
    - Search: O(n)
    - Access by index: O(n)

    Space Complexity: O(n) where n is number of nodes
    """

    def __init__(self):
        """Initialize empty linked list"""
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        """Check if list is empty"""
        return self.head is None

    def get_size(self):
        """Return number of nodes in list"""
        return self.size

    def insert_at_head(self, data):
        """
        Insert new node at beginning of list

        Args:
            data: Data to insert
        """
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self.size += 1

    def insert_at_tail(self, data):
        """
        Insert new node at end of list

        Args:
            data: Data to insert
        """
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def insert_at_position(self, position, data):
        """
        Insert new node at specific position

        Args:
            position (int): 0-based index where to insert
            data: Data to insert

        Returns:
            bool: True if successful, False if position invalid
        """
        if position < 0 or position > self.size:
            return False

        if position == 0:
            self.insert_at_head(data)
            return True

        if position == self.size:
            self.insert_at_tail(data)
            return True

        new_node = Node(data)
        current = self.head

        # Navigate to position - 1
        for i in range(position - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True

    def delete_at_head(self):
        """
        Delete first node

        Returns:
            Data of deleted node or None if empty
        """
        if self.is_empty():
            return None

        data = self.head.data

        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next

        self.size -= 1
        return data

    def delete_at_tail(self):
        """
        Delete last node

        Returns:
            Data of deleted node or None if empty
        """
        if self.is_empty():
            return None

        data = self.tail.data

        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            # Find second to last node
            current = self.head
            while current.next != self.tail:
                current = current.next

            current.next = None
            self.tail = current

        self.size -= 1
        return data

    def delete_by_value(self, value):
        """
        Delete first node with matching value

        Args:
            value: Value to search for and delete

        Returns:
            bool: True if found and deleted, False otherwise
        """
        if self.is_empty():
            return False

        # If head contains the value
        if self.head.data == value:
            self.delete_at_head()
            return True

        current = self.head
        while current.next:
            if current.next.data == value:
                # Found the node to delete
                node_to_delete = current.next
                current.next = node_to_delete.next

                # Update tail if we deleted the last node
                if node_to_delete == self.tail:
                    self.tail = current

                self.size -= 1
                return True

            current = current.next

        return False

    def search(self, value):
        """
        Search for value in list

        Args:
            value: Value to search for

        Returns:
            int: Index of first occurrence or -1 if not found
        """
        current = self.head
        index = 0

        while current:
            if current.data == value:
                return index
            current = current.next
            index += 1

        return -1

    def get_at_index(self, index):
        """
        Get data at specific index

        Args:
            index (int): 0-based index

        Returns:
            Data at index or None if index invalid
        """
        if index < 0 or index >= self.size:
            return None

        current = self.head
        for i in range(index):
            current = current.next

        return current.data

    def update_at_index(self, index, new_data):
        """
        Update data at specific index

        Args:
            index (int): 0-based index
            new_data: New data to set

        Returns:
            bool: True if successful, False if index invalid
        """
        if index < 0 or index >= self.size:
            return False

        current = self.head
        for i in range(index):
            current = current.next

        current.data = new_data
        return True

    def to_list(self):
        """
        Convert linked list to Python list

        Returns:
            list: All data in order
        """
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    def reverse(self):
        """Reverse the linked list in place"""
        prev = None
        current = self.head
        self.tail = self.head  # Old head becomes new tail

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def clear(self):
        """Remove all nodes from list"""
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        """String representation of linked list"""
        if self.is_empty():
            return "LinkedList: [] (empty)"

        items = []
        current = self.head

        while current:
            if isinstance(current.data, dict) and 'title' in current.data:
                items.append(current.data['title'])
            else:
                items.append(str(current.data))
            current = current.next

        return f"LinkedList: [{' -> '.join(items)}] (size: {self.size})"

    def __len__(self):
        """Return size of list"""
        return self.size

    def __iter__(self):
        """Make list iterable"""
        current = self.head
        while current:
            yield current.data
            current = current.next


class TaskLinkedList(LinkedList):
    """
    Specialized LinkedList for Task objects
    Extends basic LinkedList with task-specific operations
    """

    def insert_task_by_priority(self, task):
        """
        Insert task in sorted order by priority (high to low)

        Args:
            task (dict): Task dictionary with 'priority' key
        """
        if self.is_empty():
            self.insert_at_head(task)
            return

        priority = task.get('priority', 0)

        # Insert at head if higher priority than current head
        if priority > self.head.data.get('priority', 0):
            self.insert_at_head(task)
            return

        # Find correct position
        current = self.head
        position = 0

        while current and current.data.get('priority', 0) >= priority:
            current = current.next
            position += 1

        self.insert_at_position(position, task)

    def insert_task_by_due_date(self, task):
        """
        Insert task in sorted order by due date (earliest first)

        Args:
            task (dict): Task dictionary with 'due_date' key
        """
        if self.is_empty():
            self.insert_at_head(task)
            return

        due_date = task.get('due_date', '9999-12-31')

        # Insert at head if earlier due date
        if due_date < self.head.data.get('due_date', '9999-12-31'):
            self.insert_at_head(task)
            return

        # Find correct position
        current = self.head
        position = 0

        while current and current.data.get('due_date', '9999-12-31') <= due_date:
            current = current.next
            position += 1

        self.insert_at_position(position, task)

    def get_tasks_by_status(self, status):
        """
        Get all tasks with specific status

        Args:
            status (str): Status to filter by

        Returns:
            list: Tasks with matching status
        """
        result = []
        current = self.head

        while current:
            if current.data.get('status') == status:
                result.append(current.data)
            current = current.next

        return result

    def get_high_priority_tasks(self, min_priority=3):
        """
        Get all high priority tasks

        Args:
            min_priority (int): Minimum priority level

        Returns:
            list: High priority tasks
        """
        result = []
        current = self.head

        while current:
            if current.data.get('priority', 0) >= min_priority:
                result.append(current.data)
            current = current.next

        return result

    def get_overdue_tasks(self):
        """
        Get all overdue tasks

        Returns:
            list: Tasks that are past their due date
        """
        today = datetime.now().strftime('%Y-%m-%d')
        result = []
        current = self.head

        while current:
            due_date = current.data.get('due_date')
            if due_date and due_date < today and current.data.get('status') != 'completed':
                result.append(current.data)
            current = current.next

        return result

    def get_tasks_due_soon(self, days=7):
        """
        Get tasks due within specified number of days

        Args:
            days (int): Number of days to look ahead

        Returns:
            list: Tasks due within the specified timeframe
        """
        future_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        result = []
        current = self.head

        while current:
            due_date = current.data.get('due_date')
            if due_date and today <= due_date <= future_date:
                result.append(current.data)
            current = current.next

        return result

    def mark_task_complete(self, task_id):
        """
        Mark task as completed by ID

        Args:
            task_id (int): ID of task to mark complete

        Returns:
            bool: True if task found and updated
        """
        current = self.head

        while current:
            if current.data.get('id') == task_id:
                current.data['status'] = 'completed'
                current.data['completed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return True
            current = current.next

        return False

    def update_task(self, task_id, updates):
        """
        Update task with new data

        Args:
            task_id (int): ID of task to update
            updates (dict): Dictionary of fields to update

        Returns:
            bool: True if task found and updated
        """
        current = self.head

        while current:
            if current.data.get('id') == task_id:
                # Update specified fields
                for key, value in updates.items():
                    current.data[key] = value

                # Add last modified timestamp
                current.data['last_modified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return True
            current = current.next

        return False

    def delete_task_by_id(self, task_id):
        """
        Delete task by ID

        Args:
            task_id (int): ID of task to delete

        Returns:
            dict: Deleted task data or None if not found
        """
        if self.is_empty():
            return None

        # Check if head contains the task
        if self.head.data.get('id') == task_id:
            return self.delete_at_head()

        current = self.head
        while current.next:
            if current.next.data.get('id') == task_id:
                # Found the task to delete
                task_data = current.next.data
                node_to_delete = current.next
                current.next = node_to_delete.next

                # Update tail if we deleted the last node
                if node_to_delete == self.tail:
                    self.tail = current

                self.size -= 1
                return task_data

            current = current.next

        return None

    def get_task_by_id(self, task_id):
        """
        Get task by ID

        Args:
            task_id (int): ID of task to find

        Returns:
            dict: Task data or None if not found
        """
        current = self.head

        while current:
            if current.data.get('id') == task_id:
                return current.data
            current = current.next

        return None

    def get_tasks_summary(self):
        """
        Get summary statistics of all tasks

        Returns:
            dict: Summary with counts and statistics
        """
        summary = {
            'total_tasks': self.size,
            'completed': 0,
            'in_progress': 0,
            'todo': 0,
            'overdue': 0,
            'high_priority': 0,
            'due_soon': 0,
            'by_category': {}
        }

        if self.is_empty():
            return summary

        current = self.head
        today = datetime.now().strftime('%Y-%m-%d')
        future_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

        while current:
            task = current.data
            status = task.get('status', 'todo')
            due_date = task.get('due_date')
            priority = task.get('priority', 0)
            category = task.get('category', 'uncategorized')

            # Count by status
            if status == 'completed':
                summary['completed'] += 1
            elif status == 'in_progress':
                summary['in_progress'] += 1
            else:
                summary['todo'] += 1

            # Count overdue tasks
            if due_date and due_date < today and status != 'completed':
                summary['overdue'] += 1

            # Count high priority tasks
            if priority >= 3:
                summary['high_priority'] += 1

            # Count tasks due soon
            if due_date and today <= due_date <= future_date:
                summary['due_soon'] += 1

            # Count by category
            if category not in summary['by_category']:
                summary['by_category'][category] = 0
            summary['by_category'][category] += 1

            current = current.next

        return summary

    def display_tasks(self, show_completed=True):
        """
        Display all tasks in a formatted way

        Args:
            show_completed (bool): Whether to show completed tasks
        """
        if self.is_empty():
            print("No tasks found.")
            return

        current = self.head
        print(f"\n{'=' * 60}")
        print(f"{'TASK LIST':<30} {'Total: ' + str(self.size):>30}")
        print(f"{'=' * 60}")

        while current:
            task = current.data
            status = task.get('status', 'todo')

            if not show_completed and status == 'completed':
                current = current.next
                continue

            # Format task display
            task_id = task.get('id', 'N/A')
            title = task.get('title', 'Untitled')
            priority = task.get('priority', 0)
            due_date = task.get('due_date', 'No due date')
            category = task.get('category', 'uncategorized')

            # Priority indicator
            priority_indicator = '!' * min(priority, 5)

            # Status indicator
            status_indicator = {
                'completed': '✓',
                'in_progress': '⏳',
                'todo': '○'
            }.get(status, '○')

            print(f"{status_indicator} [{task_id:>3}] {title:<25} {priority_indicator:<5}")
            print(f"      Category: {category:<15} Due: {due_date}")
            print(f"      Status: {status}")
            print("-" * 60)

            current = current.next