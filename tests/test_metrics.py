import unittest
from simulation.metrics import Metrics

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = Metrics()

    def test_initial_metrics(self):
        # Check initial state
        self.assertEqual(self.metrics.total_tasks, 0)
        self.assertEqual(self.metrics.completed_tasks, 0)
        self.assertEqual(self.metrics.total_gpu_time, 0)
        self.assertEqual(self.metrics.total_transmission_time, 0)

    def test_update_metrics(self):
        # Simulate adding a task
        self.metrics.update_metrics(gpu_time=10, transmission_time=5)

        # Check updated values
        self.assertEqual(self.metrics.completed_tasks, 1)
        self.assertEqual(self.metrics.total_gpu_time, 10)
        self.assertEqual(self.metrics.total_transmission_time, 5)
        self.assertEqual(self.metrics.total_time, 15)

    def test_summarize(self):
        # Add tasks
        self.metrics.total_tasks = 5
        self.metrics.update_metrics(gpu_time=20, transmission_time=10)

        # Capture the summary output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        self.metrics.summarize()
        sys.stdout = sys.__stdout__

        # Verify the summary contains the correct data
        output = captured_output.getvalue()
        self.assertIn("Total Tasks: 5", output)
        self.assertIn("Completed Tasks: 1", output)
        self.assertIn("Total GPU Time: 20.00 seconds", output)

if __name__ == "__main__":
    unittest.main()
