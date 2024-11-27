import unittest
from models.graph_builder import GraphBuilder
from models.task_allocator import TaskAllocator

class TestTaskAllocator(unittest.TestCase):
    def setUp(self):
        self.builder = GraphBuilder()
        self.builder.add_user_node("user_1", gpu_power=5.0, bandwidth=100, latency=10)
        self.builder.add_user_node("user_2", gpu_power=2.0, bandwidth=50, latency=20)
        self.builder.add_enterprise_node("enterprise_1")
        self.builder.add_edge("user_1", "enterprise_1", bandwidth=100, latency=10)
        self.builder.add_edge("user_2", "enterprise_1", bandwidth=50, latency=20)
        self.graph = self.builder.get_graph()

        # Add a task to the enterprise
        self.graph.nodes["enterprise_1"]["data"].create_task(complexity=1e12, data_size=200)

        self.allocator = TaskAllocator(self.graph)

    def test_task_allocation(self):
        # Allocate tasks
        self.allocator.allocate_tasks()

        # Check if the task is completed
        enterprise_data = self.graph.nodes["enterprise_1"]["data"]
        self.assertTrue(enterprise_data.task_queue[0]["completed"])

    def test_no_eligible_user(self):
        # Add an unassignable task
        self.graph.nodes["enterprise_1"]["data"].create_task(complexity=1e14, data_size=500)

        # Allocate tasks
        self.allocator.allocate_tasks()

        # Verify that the task remains uncompleted
        enterprise_data = self.graph.nodes["enterprise_1"]["data"]
        uncompleted_tasks = [task for task in enterprise_data.task_queue if not task["completed"]]
        self.assertEqual(len(uncompleted_tasks), 1)

if __name__ == "__main__":
    unittest.main()
