from models.graph_builder import GraphBuilder
from models.task_allocator import TaskAllocator
import random


def generate_tasks(graph, num_tasks_per_enterprise):
    """
    Generate tasks for each enterprise in the graph.

    :param graph: The graph representing the network.
    :param num_tasks_per_enterprise: Number of tasks to generate for each enterprise.
    """
    for node, data in graph.nodes(data=True):
        if data["type"] == "enterprise":
            enterprise_node = data["data"]
            for _ in range(num_tasks_per_enterprise):
                complexity = random.uniform(1e9, 1e11)  # FLOPS
                data_size = random.uniform(50, 500)  # MB
                enterprise_node.create_task(complexity, data_size)
                print(f"Task created for {node}: {complexity:.2e} FLOPS, {data_size:.2f} MB")



def run_simulation(num_users, num_enterprises, num_tasks_per_enterprise):
    """
    Run a simulation with the specified parameters.

    :param num_users: Number of user nodes.
    :param num_enterprises: Number of enterprise nodes.
    :param num_tasks_per_enterprise: Number of tasks to generate per enterprise.
    """
    # Step 1: Build the graph
    print("Building graph...")
    builder = GraphBuilder()
    builder.create_random_graph(num_users, num_enterprises, connection_probability=0.3)
    graph = builder.get_graph()
    print(f"Graph created with {num_users} users and {num_enterprises} enterprises.")

    # Step 2: Generate tasks for enterprises
    print("Generating tasks...")
    generate_tasks(graph, num_tasks_per_enterprise)

    # Step 3: Allocate tasks
    print("Allocating tasks...")
    allocator = TaskAllocator(graph)
    allocator.allocate_tasks()

    # Step 4: Collect and summarize results
    print("Simulation complete. Summary:")
    for node, data in graph.nodes(data=True):
        if data["type"] == "enterprise":
            pending_tasks = len(data["data"].get_pending_tasks())
            completed_tasks = len(data["data"].task_queue) - pending_tasks
            print(
                f"{node}: {completed_tasks} tasks completed, {pending_tasks} tasks pending."
            )

    return graph

