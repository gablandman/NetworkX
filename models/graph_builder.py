import networkx as nx
import random
from models.user_node import UserNode
from models.enterprise_node import EnterpriseNode


class GraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_user_node(self, node_id, gpu_power, bandwidth, latency):
        """
        Add a user node to the graph.

        :param node_id: Unique identifier for the user node.
        :param gpu_power: GPU power in TFLOPS.
        :param bandwidth: Network bandwidth in Mbps.
        :param latency: Network latency in ms.
        """
        user_node = UserNode(node_id, gpu_power, bandwidth, latency)
        self.graph.add_node(node_id, data=user_node, type="user")

    def add_enterprise_node(self, node_id):
        """
        Add an enterprise node to the graph.

        :param node_id: Unique identifier for the enterprise node.
        """
        enterprise_node = EnterpriseNode(node_id)
        self.graph.add_node(node_id, data=enterprise_node, type="enterprise")

    def add_edge(self, user_node_id, enterprise_node_id, bandwidth, latency):
        """
        Add an edge between a user node and an enterprise node.

        :param user_node_id: The user node's identifier.
        :param enterprise_node_id: The enterprise node's identifier.
        :param bandwidth: Bandwidth of the connection in Mbps.
        :param latency: Latency of the connection in ms.
        """
        self.graph.add_edge(
            user_node_id,
            enterprise_node_id,
            bandwidth=bandwidth,
            latency=latency,
        )

    def create_random_graph(self, num_users, num_enterprises, connection_probability=0.9):
        """
        Generate a random graph with specified numbers of users and enterprises.

        :param num_users: Number of user nodes.
        :param num_enterprises: Number of enterprise nodes.
        :param connection_probability: Probability of a connection between a user and an enterprise.
        """
        for i in range(num_users):
            self.add_user_node(
                node_id=f"user_{i}",
                gpu_power=random.uniform(1.5, 3.0),  # Random GPU power in TFLOPS
                bandwidth=random.randint(10, 100),  # Random bandwidth in Mbps
                latency=random.randint(10, 50),  # Random latency in ms
            )

        for j in range(num_enterprises):
            self.add_enterprise_node(node_id=f"enterprise_{j}")

        # Add edges with a given connection probability
        user_nodes = [node for node, data in self.graph.nodes(data=True) if data["type"] == "user"]
        enterprise_nodes = [node for node, data in self.graph.nodes(data=True) if data["type"] == "enterprise"]

        for user_node in user_nodes:
            for enterprise_node in enterprise_nodes:
                if random.random() < connection_probability:
                    self.add_edge(
                        user_node_id=user_node,
                        enterprise_node_id=enterprise_node,
                        bandwidth=random.randint(10, 100),  # Random bandwidth in Mbps
                        latency=random.randint(10, 50),  # Random latency in ms
                    )

    def get_graph(self):
        """
        Get the generated graph.

        :return: The graph.
        """
        return self.graph
