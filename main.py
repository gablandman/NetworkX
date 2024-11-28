from models.event_manager import EventManager
from models.task_allocator import TaskAllocator
from models.graph_builder import  GraphBuilder
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
                complexity = random.uniform(1e9, 1e11)  # FLOPS
                data_size = random.uniform(50, 500)  # MB
                enterprise_node.create_task(complexity, data_size)
                print(f"Task created for {node}: {complexity:.2e} FLOPS, {data_size:.2f} MB")


def main():
    builder = GraphBuilder()
    builder.create_random_graph(10, 3, connection_probability=0.3)
    graph = builder.get_graph()

    event_manager = EventManager()
    allocator = TaskAllocator(graph, event_manager)

    # Generate and allocate tasks
    generate_tasks(graph, 5)
    allocator.allocate_tasks()

    # Initialize the simulator
    events = event_manager.get_events()
    simulator = DynamicSimulator(graph, events)
    
    simulator.run()

if __name__ == "__main__":
    main()
