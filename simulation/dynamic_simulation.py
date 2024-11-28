import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx
import random


class DynamicSimulator:
    """
    Simulates the graph dynamically by processing events.
    """
    def __init__(self, graph, events):
        """
        Initialize the simulator.

        :param graph: The initial graph.
        :param events: List of events to simulate.
        """
        self.graph = graph
        self.events = events
        self.current_index = 0

        # Fixed positions for nodes
        self.positions = self._generate_fixed_positions()

    def _generate_fixed_positions(self):
        """
        Generate fixed positions for nodes: enterprises on top, users dispersed at the bottom.
        """
        positions = {}
        users = [n for n, d in self.graph.nodes(data=True) if d["type"] == "user"]
        enterprises = [n for n, d in self.graph.nodes(data=True) if d["type"] == "enterprise"]

        # Position enterprises in a horizontal line at the top
        for i, enterprise in enumerate(enterprises):
            positions[enterprise] = (i * 2, 5)  # Space enterprises equally

        # Position users dispersed randomly at the bottom
        for user in users:
            positions[user] = (random.uniform(-5, 10), random.uniform(-5, -3))

        return positions

    def next_frame(self, event=None):
        """
        Process the next event and update the graph.
        """
        if self.current_index >= len(self.events):
            print("Simulation complete.")
            return

        event = self.events[self.current_index]

        if event["type"] == "data_transmission":
            self._handle_data_transmission(event)
        elif event["type"] == "calculation":
            self._handle_calculation(event)
        elif event["type"] == "remove_edge":
            self._handle_remove_edge(event)

        self.current_index += 1
        self._draw_graph(event)

    def _handle_data_transmission(self, event):
        from_node, to_node = event["from_node"], event["to_node"]
        size = event["size"]

        if not self.graph.has_edge(from_node, to_node):
            self.graph.add_edge(
                from_node, to_node, weight=size
            )

        print(f"Transmission from {from_node} to {to_node}, Size: {size} MB")

    def _handle_start_calculation(self, event):
        print(f"Calculation started on {event['node']}")

    def _handle_calculation(self, event):
        """
        Handle the calculation event.
        """
        node = event["node"]
        print(f"Node {node} is performing a calculation.")

    def _handle_end_calculation(self, event):
        """
        Handle the end of a calculation event.
        """
        node = event["node"]
        print(f"Calculation ended on {node}")

        # Remove the edge used in the current event
        edge = event.get("edge")
        if edge in self.graph.edges:
            self.graph.remove_edge(*edge)

        # Special case: If this is the last edge returning to the enterprise, remove it
        if event["type"] == "data_transmission" and edge[1] in [
            n for n, d in self.graph.nodes(data=True) if d["type"] == "enterprise"
        ]:
            if edge in self.graph.edges:
                self.graph.remove_edge(*edge)

    def _handle_remove_edge(self, event):
        """
        Handle the removal of an edge.
        """
        edge = event["edge"]
        if edge in self.graph.edges:
            print(f"Removing edge: {edge}")
            self.graph.remove_edge(*edge)

    def _add_temporary_edge(self, edge):
        """
        Add an edge temporarily to the graph for visualization.
        """
        if not self.graph.has_edge(*edge):
            self.graph.add_edge(
                edge[0], edge[1],
                bandwidth=random.randint(10, 100),  # Random bandwidth
                latency=random.randint(10, 50)     # Random latency
        )

    def _draw_graph(self, event):
        """
        Draw the graph dynamically with updated edges and colors.
        """
        plt.clf()  # Clear the current figure

        # Get active edges from the current event
        active_edges = [event["edge"]] if "edge" in event else []
        active_node = event["node"] if "node" in event else None

        # Create a subgraph with only the active edges
        temp_graph = nx.DiGraph()
        temp_graph.add_nodes_from(self.graph.nodes(data=True))
        temp_graph.add_edges_from(active_edges)

        # Highlight the active edges
        edge_colors = ["blue" for edge in temp_graph.edges]
        edge_widths = [2 for edge in temp_graph.edges]

        # Color nodes based on their type and activity
        node_colors = []
        for node, data in temp_graph.nodes(data=True):
            if node == active_node:
                node_colors.append("yellow")  # Highlight the active node
            elif data["type"] == "enterprise":
                node_colors.append("red")
            else:
                node_colors.append("green")

        nx.draw(
            temp_graph,
            pos=self.positions,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            width=edge_widths,
            node_size=800,
        )
        edge_labels = nx.get_edge_attributes(self.graph, "bandwidth")
        nx.draw_networkx_edge_labels(self.graph, pos=self.positions, edge_labels=edge_labels)
        plt.title(f"Event: {event['type']} (Node: {active_node}, Edge: {event.get('edge')})")
        plt.draw()


    def run(self):
        """
        Run the simulator with a button for advancing frames.
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.25)  # Leave more space for the button

        # Add a "Next Frame" button
        ax_button = plt.axes([0.75, 0.05, 0.2, 0.1])  # Adjust size and position
        button = Button(ax_button, "Next Frame", color='lightblue', hovercolor='lightgreen')
        button.on_clicked(self.next_frame)

        # Initial draw
        self._draw_graph({"type": "Initialization"})
        plt.show()
