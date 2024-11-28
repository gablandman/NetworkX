class TaskAllocator:
    """
    Manages the allocation of tasks from enterprise nodes to user nodes.
    """
    def __init__(self, graph, event_manager):
        """
        Initialize the TaskAllocator with a graph and event manager.

        :param graph: The graph representing the network.
        :param event_manager: The event manager for tracking events.
        """
        self.graph = graph
        self.event_manager = event_manager
        self.current_time = 0

    def allocate_tasks(self):
        """
        Allocate tasks from enterprises to users and generate events.
        """
        for enterprise, data in self.graph.nodes(data=True):
            if data["type"] == "enterprise":
                enterprise_node = data["data"]
                tasks = enterprise_node.get_pending_tasks()

                for task in tasks:
                    self._assign_task(enterprise, task)

    def _assign_task(self, enterprise_id, task):
        """
        Assign a task to a suitable user node and generate events.

        :param enterprise_id: The enterprise node generating the task.
        :param task: The task to be assigned.
        """
        candidates = [
            (user, edge_data)
            for user, entreprise, edge_data in self.graph.in_edges(enterprise_id, data=True)
            if self.graph.nodes[user]["data"].gpu_power * 1e12 >= task["complexity"]
        ]

        if not candidates:
            print(f"No suitable user nodes found for task from {enterprise_id}")
            return

        # Select user with the lowest latency
        best_user, best_edge_data = min(candidates, key=lambda x: x[1]["latency"])
        self._process_task(best_user, enterprise_id, task, best_edge_data)

    def _process_task(self, user_id, enterprise_id, task, edge_data):
        """
        Simulate processing a task by a user node and generate events.

        :param user_id: The user node processing the task.
        :param enterprise_id: The enterprise node assigning the task.
        :param task: The task being processed.
        :param edge_data: Edge data between user and enterprise.
        """
        gpu_time = task["complexity"] / (self.graph.nodes[user_id]["data"].gpu_power * 1e12)
        transmission_time = task["data_size"] / edge_data["bandwidth"]
        total_time = gpu_time + transmission_time

        # Generate events
        self.event_manager.add_event(self.current_time, "start_calculation", node=user_id, task=task)
        self.event_manager.add_event(
            self.current_time + transmission_time, "data_transmission", from_node=enterprise_id, to_node=user_id, size=task["data_size"]
        )
        self.event_manager.add_event(self.current_time + total_time, "end_calculation", node=user_id, task=task)

        # Update task state
        task["completed"] = True
        task["gpu_time"] = gpu_time
        task["transmission_time"] = transmission_time
        self.current_time += total_time  # Increment time for this task
        print(
            f"Task from {enterprise_id} completed by {user_id}: "
            f"GPU Time = {gpu_time:.2f}s, Transmission Time = {transmission_time:.2f}s, Total Time = {total_time:.2f}s"
        )
