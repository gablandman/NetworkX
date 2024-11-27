class UserNode:
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
        self.tasks_processed = 0

    def process_task(self, task_complexity):
        """
        Simulate task processing by the user node.

        :param task_complexity: Computational complexity of the task in FLOPS.
        :return: Time taken to process the task in seconds.
        """
        return task_complexity / (self.gpu_power * 1e12)

    def __repr__(self):
        return (
            f"UserNode({self.node_id}, GPU: {self.gpu_power} TFLOPS, "
            f"Bandwidth: {self.bandwidth} Mbps, Latency: {self.latency} ms)"
        )
