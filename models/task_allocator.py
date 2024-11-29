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
        Allocate tasks from all enterprises to users, allowing parallel chains.
        """
        tasks_to_allocate = []  # Collect tasks from all enterprises

        for enterprise, data in self.graph.nodes(data=True):
            if data["type"] == "enterprise":
                enterprise_node = data["data"]
                tasks = enterprise_node.get_pending_tasks()
                tasks_to_allocate.extend([(enterprise, task) for task in tasks])

        # Shuffle tasks to mix enterprises (optional, to improve fairness)
        random.shuffle(tasks_to_allocate)

        # Allocate tasks
        for enterprise, task in tasks_to_allocate:
            available_users = [
                (user, self.graph.nodes[user]["data"])
                for user in self.graph.nodes
                if self.graph.nodes[user]["type"] == "user"
            ]
            available_users = sorted(
                available_users,
                key=lambda x: x[1].get_priority()
            )[:d]

            print(f"available users : {[( available_user[1].node_id,available_user[1].queue) for available_user in available_users]}")


            if len(available_users) < d:
                print(f"Not enough devices available for chain from {enterprise}")
                continue

            # Assign the task to the chain of users
            self._assign_chain(enterprise, task, available_users)



    def _assign_chain(self, enterprise_id, task, chain_users):
        """
        Assign a chain of devices to process a task, prioritizing users with shorter queues.
        """
        previous_node = enterprise_id
        portion_size = task["complexity"] / len(chain_users)
        current_time = self.current_time

        for i, (node_id, user_data) in enumerate(chain_users):
            transmission_time = task["data_size"] / random.randint(10, 100)  # Simulated bandwidth
            gpu_time = portion_size / (user_data.gpu_power * 1e12)

            # Add task to user's queue
            user_task = {
                "portion": portion_size,
                "data_size": task["data_size"], #a corrriger 
                "duration": gpu_time #a corrriger 
            }
            user_data.add_task(user_task, current_time + transmission_time)

            # Transmission to the user
            edge_to_user = (previous_node, node_id)
            self.event_manager.add_event(
                current_time + transmission_time,
                "data_transmission",
                from_node=previous_node,
                to_node=node_id,
                size=task["data_size"],
                edge=edge_to_user
            )

            # Calculation at the user
            self.event_manager.add_event(
                current_time + transmission_time + gpu_time,
                "calculation",
                node=node_id,
                task={"portion": portion_size, "total_task": task},
                edge=edge_to_user
            )

            # Update current time for this chain
            current_time += transmission_time + gpu_time
            previous_node = node_id

        # Transmission back to the enterprise
        edge_to_enterprise = (previous_node, enterprise_id)
        self.event_manager.add_event(
            current_time,
            "data_transmission",
            from_node=previous_node,
            to_node=enterprise_id,
            size=task["data_size"],
            edge=edge_to_enterprise
        )
