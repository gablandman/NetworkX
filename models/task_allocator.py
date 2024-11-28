import random

class TaskAllocator:
    """
    Manages the allocation of tasks from enterprise nodes to user nodes in a sequential manner.
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

    def allocate_tasks(self, d=3):
        """
        Allocate tasks from enterprises to users in chains of size d.

        :param d: Number of devices in the chain.
        """
        for enterprise, data in self.graph.nodes(data=True):
            if data["type"] == "enterprise":
                enterprise_node = data["data"]
                tasks = enterprise_node.get_pending_tasks()

                for task in tasks:
                    self._assign_chain(enterprise, task, d)

    def _assign_chain(self, enterprise_id, task, d):
        """
        Dynamically assign a chain of devices for processing a task.
        """
        # Select d devices dynamically
        candidates = [
            (user, self.graph.nodes[user]["data"])
            for user in self.graph.nodes
            if self.graph.nodes[user]["type"] == "user"
        ]
        candidates = sorted(candidates, key=lambda x: (len(x[1].queue), -x[1].gpu_power))[:d]

        if len(candidates) < d:
            print(f"Not enough devices for chain processing from {enterprise_id}")
            return

        previous_node = enterprise_id
        portion_size = task["complexity"] / d

        for i, (node_id, user_data) in enumerate(candidates):
            # Simulate transmission and calculation times
            transmission_time = task["data_size"] / random.randint(10, 100)  # Simulated bandwidth
            gpu_time = portion_size / (user_data.gpu_power * 1e12)

            # Generate events for the edge
            edge = (previous_node, node_id)
            self.event_manager.add_event(
                self.current_time + transmission_time,
                "data_transmission",
                from_node=previous_node,
                to_node=node_id,
                size=task["data_size"],
                edge=edge  # Specify the active edge
            )
            self.event_manager.add_event(
                self.current_time + transmission_time + gpu_time,
                "calculation",
                node=node_id,
                task={"portion": portion_size, "total_task": task},
                edge=edge  # Specify the active edge
            )

            self.current_time += transmission_time + gpu_time
            previous_node = node_id

        # Final transmission back to the enterprise
        final_edge = (previous_node, enterprise_id)
        self.event_manager.add_event(
            self.current_time,
            "data_transmission",
            from_node=previous_node,
            to_node=enterprise_id,
            size=task["data_size"],
            edge=final_edge  # Specify the active edge
        )
