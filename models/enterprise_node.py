class EnterpriseNode:
    def __init__(self, node_id):
        """
        Initialize the enterprise node.

        :param node_id: Unique identifier for the enterprise node.
        """
        self.node_id = node_id
        self.task_queue = []

    def create_task(self, complexity, data_size):
        """
        Add a new task to the enterprise's task queue.

        :param complexity: Computational complexity of the task in FLOPS.
        :param data_size: Data size associated with the task in MB.
        """
        task = {
            "complexity": complexity,
            "data_size": data_size,
            "completed": False
        }
        self.task_queue.append(task)

    def get_pending_tasks(self):
        """
        Get all pending tasks in the task queue.

        :return: List of pending tasks.
        """
        return [task for task in self.task_queue if not task["completed"]]

    def mark_task_completed(self, task):
        """
        Mark a specific task as completed.

        :param task: The task to mark as completed.
        """
        task["completed"] = True

    def __repr__(self):
        return f"EnterpriseNode({self.node_id}, Pending Tasks: {len(self.get_pending_tasks())})"
