class UserNode:
    """
    Represents a user node in the graph (e.g., an iPhone with GPU capabilities).
    """
    def __init__(self, node_id, gpu_power, bandwidth, latency):
        """
        Initialize the user node.

        :param node_id: Unique identifier for the user node.
        :param gpu_power: GPU power in TFLOPS.
        :param bandwidth: Network bandwidth in Mbps.
        :param latency: Network latency in ms.
        """
        self.node_id = node_id
        self.gpu_power = gpu_power  # TFLOPS
        self.bandwidth = bandwidth  # Mbps
        self.latency = latency  # ms
        self.queue = []  # Queue for tasks
        self.active = False  # Whether the node is currently processing a task

    def add_to_queue(self, task):
        """
        Add a task to the node's queue.

        :param task: The task to add.
        """
        self.queue.append(task)

    def process_queue(self):
        """
        Process the next task in the queue if the node is inactive.

        :return: The task being processed or None if the queue is empty.
        """
        if not self.active and self.queue:
            task = self.queue.pop(0)
            self.active = True
            return task
        return None

    def complete_task(self):
        """
        Mark the current task as complete and set the node to inactive.
        """
        self.active = False

    def __repr__(self):
        return (
            f"UserNode({self.node_id}, GPU: {self.gpu_power} TFLOPS, "
            f"Bandwidth: {self.bandwidth} Mbps, Latency: {self.latency} ms, "
            f"Queue: {len(self.queue)} tasks)"
        )
