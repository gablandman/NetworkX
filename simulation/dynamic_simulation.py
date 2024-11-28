import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import networkx as nx
import random


class DynamicSimulator:
    """
    Simulates the graph dynamically by processing events.
    """
    def __init__(self, graph, event_manager):
        """
        Initialize the simulator.

        :param graph: The initial graph.
        :param event_manager: The event manager containing the global timeline of events.
        """
        self.graph = graph
        self.event_manager = event_manager  # Store the event manager
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
        Process the next event in the global timeline and update the graph.
        """
        next_event = self.event_manager.get_next_event()
        if not next_event:
            print("Simulation complete.")
            return

        if next_event["type"] == "data_transmission":
            self._handle_data_transmission(next_event)
        elif next_event["type"] == "calculation":
            self._handle_calculation(next_event)

        self._draw_graph(next_event)



    def _handle_data_transmission(self, event):
        """
        Handle the transmission of data.
        """
        from_node, to_node = event["from_node"], event["to_node"]
        size = event["size"]

        # Ensure the edge exists temporarily
        if not self.graph.has_edge(from_node, to_node):
            self.graph.add_edge(
                from_node, to_node,
                bandwidth=random.randint(10, 100)  # Assign random bandwidth
            )

        # Get bandwidth and calculate transmission time
        bandwidth = self.graph.edges[from_node, to_node]["bandwidth"]
        transmission_time = size / bandwidth

        print(f"Transmission from {from_node} to {to_node}, Size: {size:.2f} MB, "
            f"Bandwidth: {bandwidth} Mbps, Time: {transmission_time:.2f} seconds.")

            # Remove the edge after the event
        #self.graph.remove_edge(from_node, to_node)

    def _handle_calculation(self, event):
        """
        Handle the calculation event.
        """
        node = event["node"]
        task = event["task"]
        gpu_power = self.graph.nodes[node]["data"].gpu_power  # GPU power in TFLOPS
        portion = task["portion"]

        # Calculate calculation time
        calculation_time = portion / (gpu_power * 1e12)

        print(f"Node {node} is performing a calculation, Portion: {portion:.2e} FLOPS, "
            f"GPU Power: {gpu_power:.2f} TFLOPS, Time: {calculation_time:.2f} seconds.")



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
        plt.clf()

        # Highlight active edges and nodes
        active_edges = [event["edge"]] if "edge" in event else []
        active_node = event["node"] if "node" in event else None

        edge_colors = ["blue" if edge in active_edges else "gray" for edge in self.graph.edges]
        edge_widths = [2 if edge in active_edges else 0.5 for edge in self.graph.edges]

        node_colors = []
        for node, data in self.graph.nodes(data=True):
            if node == active_node:
                node_colors.append("yellow")
            elif data["type"] == "enterprise":
                node_colors.append("red")
            else:
                node_colors.append("green")

        nx.draw(
            self.graph,
            pos=self.positions,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            width=edge_widths,
            node_size=800,
        )

        # Extract the current simulation time from the event
        current_time = event["time"] if "time" in event else 0

        # Add a legend showing the elapsed time and current event
        legend_text = (f"Simulation Time: {current_time:.2f} seconds\n"
                    f"Event: {event['type']}\n"
                    f"Node: {active_node or 'None'}\n"
                    f"Edge: {event.get('edge') or 'None'}")
        plt.gca().legend([legend_text], loc='upper right', frameon=False, fontsize=10)

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
