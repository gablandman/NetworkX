import matplotlib.pyplot as plt
import networkx as nx


def plot_graph(graph):
    """
    Plot the graph with node types and edge attributes.

    :param graph: The graph to plot.
    """
    pos = nx.spring_layout(graph)
    node_colors = [
        "blue" if data["type"] == "user" else "green" for _, data in graph.nodes(data=True)
    ]
    edge_labels = {
        (u, v): f'{data["bandwidth"]} Mbps\n{data["latency"]} ms'
        for u, v, data in graph.edges(data=True)
    }

    plt.figure(figsize=(20, 10))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=1000,
        node_color=node_colors,
        font_size=6,
        font_color="black",
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=5)
    plt.title("Graph Visualization")
    plt.show()


def plot_metrics(metrics):
    """
    Plot metrics collected during the simulation.

    :param metrics: The Metrics object with collected data.
    """
    labels = ["GPU Time", "Transmission Time", "Total Time"]
    values = [
        metrics.total_gpu_time,
        metrics.total_transmission_time,
        metrics.total_time,
    ]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=["orange", "blue", "green"])
    plt.ylabel("Time (seconds)")
    plt.title("Metrics Summary")
    plt.show()
