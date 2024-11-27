class TaskAllocator:

    def __init__(self, graph):
        """
        Initialize the TaskAllocator with a graph.

        :param graph: The graph representing the network.
        """
        self.graph = graph

    def allocate_tasks(self):
        """
        Allocate tasks from enterprises to users based on available resources.
        """
        for enterprise, data in self.graph.nodes(data=True):
            if data["type"] == "enterprise":
                enterprise_node = data["data"]
                tasks = enterprise_node.get_pending_tasks()

                for task in tasks:
                    self._assign_task(enterprise, task)

    def _assign_task(self, enterprise_id, task):
        """
        Assign a task to a suitable user node.

        :param enterprise_id: The enterprise node generating the task.
        :param task: The task to be assigned.
        """
        candidates = []
        for user, entreprise, edge_data in self.graph.in_edges(enterprise_id, data=True):
            gpu_power = self.graph.nodes[user]["data"].gpu_power
            if gpu_power * 1e12 >= task["complexity"]:
                candidates.append((user, edge_data))

        if not candidates:
            print(f"No suitable user nodes for task from {enterprise_id}: {task}")
            return  # Skip this task if no users are connected or eligible

        # Select user with the lowest latency
        best_user, best_edge_data = min(candidates, key=lambda x: x[1]["latency"])
        self._process_task(best_user, enterprise_id, task, best_edge_data)


    def _process_task(self, user_id, enterprise_id, task, edge_data):
        """
        Simulate processing a task by a user node.

        :param user_id: The user node processing the task.
        :param enterprise_id: The enterprise node assigning the task.
        :param task: The task being processed.
        :param edge_data: Edge data between user and enterprise.
        """
        user_node = self.graph.nodes[user_id]["data"]
        gpu_time = user_node.process_task(task["complexity"])
        transmission_time = task["data_size"] / edge_data["bandwidth"]

        total_time = gpu_time + transmission_time
        task["completed"] = True
        task["gpu_time"] = gpu_time
        task["transmission_time"] = transmission_time
        
        print(
            f"Task from {enterprise_id} completed by {user_id}: "
            f"GPU Time = {gpu_time:.2f}s, Transmission Time = {transmission_time:.2f}s, Total Time = {total_time:.2f}s"
        )
