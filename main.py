from models.event_manager import EventManager
from models.task_allocator import TaskAllocator
from models.graph_builder import GraphBuilder
from simulation.dynamic_simulation import DynamicSimulator
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
                complexity = random.uniform(1e10, 5e11)  # Reduced FLOPS
                data_size = random.uniform(5, 50)  # Reduced MB
                enterprise_node.create_task(complexity, data_size)
                print(f"Task created for {node}: {complexity:.2e} FLOPS, {data_size:.2f} MB")



def main():
    """
    Main function to set up and run the simulation.
    """
    # Step 1: Build the graph
    builder = GraphBuilder()
    builder.create_empty_graph(40, 7)  # 40 users, 3 enterprises
    graph = builder.get_graph()

    # Step 2: Initialize EventManager and TaskAllocator
    event_manager = EventManager()
    allocator = TaskAllocator(graph, event_manager)

    # Step 3: Generate tasks for the enterprises
    generate_tasks(graph, 2)  # Generate 2 tasks per enterprise

    # Step 4: Allocate tasks (events added to timeline dynamically)
    allocator.allocate_tasks()

    # Step 5: Initialize the simulator with the event manager
    simulator = DynamicSimulator(graph, event_manager)

    # Step 6: Run the interactive simulation
    simulator.run()


if __name__ == "__main__":
    main()

