class UserNode:
    """
    Represents a user node in the graph (e.g., an iPhone with GPU capabilities).
    """
    def __init__(self, node_id, gpu_power, bandwidth, latency):
        self.node_id = node_id
        self.gpu_power = gpu_power * 0.05  # Reduce GPU power by a factor
        self.bandwidth = bandwidth
        self.latency = latency
        self.queue = []  # Queue for tasks
        self.active_task = None  # Current task being processed


    def add_task(self, task, start_time):
        """
        Add a task to the user's queue.
        """
        self.queue.append((task, start_time))

    def process_next_task(self, current_time):
        """
        Process the next task in the queue if available.
        """
        if self.active_task is None and self.queue:
            self.active_task, start_time = self.queue.pop(0)
            completion_time = current_time + self.active_task["duration"]
            return self.active_task, completion_time
        return None, None

    def complete_task(self):
        """
        Mark the current task as complete.
        """
        self.active_task = None
