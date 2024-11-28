import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx


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
        Generate fixed positions for nodes: enterprises on top, users at the bottom.
        """
        positions = {}
        users = [n for n, d in self.graph.nodes(data=True) if d["type"] == "user"]
        enterprises = [n for n, d in self.graph.nodes(data=True) if d["type"] == "enterprise"]

        # Position enterprises on top
        for i, enterprise in enumerate(enterprises):
            positions[enterprise] = (i, 2)

        # Position users at the bottom
        for j, user in enumerate(users):
            positions[user] = (j, 0)

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
        elif event["type"] == "start_calculation":
            self._handle_start_calculation(event)
        elif event["type"] == "end_calculation":
            self._handle_end_calculation(event)

        self.current_index += 1
        self._draw_graph(event)

    def _handle_data_transmission(self, event):
        from_node, to_node = event["from_node"], event["to_node"]
        size = event["size"]

        if not self.graph.has_edge(from_node, to_node):
            self.graph.add_edge(from_node, to_node, weight=size)

        print(f"Transmission from {from_node} to {to_node}, Size: {size} MB")

    def _handle_start_calculation(self, event):
        print(f"Calculation started on {event['node']}")

    def _handle_end_calculation(self, event):
        print(f"Calculation ended on {event['node']}")

    def _draw_graph(self, event):
        plt.clf()  # Clear the current figure

        node_colors = [
            "red" if d["type"] == "enterprise" else "green" for _, d in self.graph.nodes(data=True)
        ]
        edge_colors = [
            "blue" if (event.get("from_node"), event.get("to_node")) == edge[:2] else "gray"
            for edge in self.graph.edges
        ]

        nx.draw(
            self.graph,
            pos=self.positions,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=800,
        )
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos=self.positions, edge_labels=edge_labels)
        plt.title(f"Event: {event['type']}")
        plt.draw()

    def run(self):
        """
        Run the simulator with a button for advancing frames.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)

        # Add a "Next" button
        ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])  # Position of the button
        button = Button(ax_button, "Next Frame")
        button.on_clicked(self.next_frame)

        # Initial draw
        self._draw_graph({"type": "Initialization"})
        plt.show()
