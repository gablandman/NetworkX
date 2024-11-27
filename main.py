from simulation.run_simulation import run_simulation
from simulation.metrics import Metrics, calculate_metrics
from simulation.visualization import plot_graph, plot_metrics


def main():
    """
    Main entry point for running the simulation.
    """
    # Parameters for the simulation
    NUM_USERS = 40  # Number of user nodes
    NUM_ENTERPRISES = 10  # Number of enterprise nodes
    NUM_TASKS_PER_ENTERPRISE = 3  # Number of tasks per enterprise

    print("\n=== Starting Simulation ===\n")

    # Step 1: Run the simulation
    graph = run_simulation(NUM_USERS, NUM_ENTERPRISES, NUM_TASKS_PER_ENTERPRISE)

    # Step 2: Calculate metrics
    print("\n=== Calculating Metrics ===\n")
    metrics = Metrics()
    calculate_metrics(graph, metrics)
    metrics.summarize()
    # Step 3: Visualize the results
    print("\n=== Visualizing Results ===\n")
    plot_graph(graph)
    plot_metrics(metrics)


if __name__ == "__main__":
    main()
