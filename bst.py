class TaskNode:
    def __init__(self, task):
        self.task = task
        self.left = None#stores the task, and left and right pointers
        self.right = None

class BST:#handles traversal, insertion and search
    def __init__(self):#stores nodes
        self.root = None

    def insert(self, task):
        def _insert(node, task):
            if not node:
                return TaskNode(task)#creates a new node
            if task.priority < node.task.priority:
                node.left = _insert(node.left, task)#moves to  the left if the task is of lower priority than  the node.task
            else:
                node.right = _insert(node.right, task)#moves right instead
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
            if node.task.priority == priority:#sets the root node as the priority
                return node.task
            elif priority < node.task.priority:
                return _search(node.left, priority)
            else:
                return _search(node.right, priority)
        return _search(self.root, priority)
  