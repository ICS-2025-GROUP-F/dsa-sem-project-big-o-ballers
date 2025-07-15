class TaskNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, task):
        def _insert(node, task):
            if not node:
                return TaskNode(task)
            if task['priority'] < node.task['priority']:
                node.left = _insert(node.left, task)
            else:
                node.right = _insert(node.right, task)
            return node
        self.root = _insert(self.root, task)

    def inorder_traversal(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.task)
                _inorder(node.right)
        _inorder(self.root)
        return result

    def search(self, priority):
        def _search(node, priority):
            if not node:
                return None
            if node.task['priority'] == priority:
                return node.task
            elif priority < node.task['priority']:
                return _search(node.left, priority)
            else:
                return _search(node.right, priority)
        return _search(self.root, priority)
