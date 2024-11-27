import unittest
from models.graph_builder import GraphBuilder

class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = GraphBuilder()

    def test_create_random_graph(self):
        # Create a small random graph
        self.builder.create_random_graph(num_users=5, num_enterprises=2, connection_probability=0.5)
        graph = self.builder.get_graph()

        # Check the number of nodes
        self.assertEqual(len(graph.nodes), 7)  # 5 users + 2 enterprises

        # Check that nodes have correct types
        for node, data in graph.nodes(data=True):
            self.assertIn(data["type"], ["user", "enterprise"])

        # Check if edges exist
        user_nodes = [n for n, d in graph.nodes(data=True) if d["type"] == "user"]
        enterprise_nodes = [n for n, d in graph.nodes(data=True) if d["type"] == "enterprise"]
        connected = any(graph.has_edge(u, e) for u in user_nodes for e in enterprise_nodes)
        self.assertTrue(connected)

    def test_add_edge_properties(self):
        # Add nodes and edges manually
        self.builder.add_user_node("user_1", gpu_power=3.0, bandwidth=50, latency=10)
        self.builder.add_enterprise_node("enterprise_1")
        self.builder.add_edge("user_1", "enterprise_1", bandwidth=50, latency=20)

        graph = self.builder.get_graph()
        edge_data = graph["user_1"]["enterprise_1"]

        # Check edge properties
        self.assertEqual(edge_data["bandwidth"], 50)
        self.assertEqual(edge_data["latency"], 20)

if __name__ == "__main__":
    unittest.main()
