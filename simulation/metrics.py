class Metrics:
    
    def __init__(self):
        self.total_tasks = 0
        self.completed_tasks = 0
        self.total_gpu_time = 0
        self.total_transmission_time = 0
        self.total_time = 0

    def update_metrics(self, gpu_time, transmission_time):
        """
        Update the metrics for a completed task.

        :param gpu_time: Time spent on GPU computation (seconds).
        :param transmission_time: Time spent on data transmission (seconds).
        """
        self.completed_tasks += 1
        self.total_gpu_time += gpu_time
        self.total_transmission_time += transmission_time
        self.total_time += gpu_time + transmission_time

    def summarize(self):
        """
        Print a summary of the metrics.
        """
        print("\nMetrics Summary:")
        print(f"Total Tasks: {self.total_tasks}")
        print(f"Completed Tasks: {self.completed_tasks}")
        print(f"Total GPU Time: {self.total_gpu_time:.2f} seconds")
        print(f"Total Transmission Time: {self.total_transmission_time:.2f} seconds")
        print(f"Total Time (GPU + Transmission): {self.total_time:.2f} seconds")
        print(f"Completion Rate: {self.completed_tasks / self.total_tasks * 100:.2f}%\n")


def calculate_metrics(graph, metrics):
    """
    Calculate metrics for a graph after task allocation and processing.

    :param graph: The graph representing the network.
    :param metrics: A Metrics object to collect data.
    """
    for node, data in graph.nodes(data=True):
        if data["type"] == "enterprise":
            enterprise_node = data["data"]
            metrics.total_tasks += len(enterprise_node.task_queue)
            for task in enterprise_node.task_queue:
                if task["completed"]:
                    print(task)
                    gpu_time = task.get("gpu_time", 0)
                    transmission_time = task.get("transmission_time", 0)
                    metrics.update_metrics(gpu_time, transmission_time)
