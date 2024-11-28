class EventManager:
    """
    Manages a global timeline of events during the simulation.
    """
    def __init__(self):
        self.events = []

    def add_event(self, time, event_type, **kwargs):
        """
        Add a new event to the timeline.

        :param time: Timestamp of the event.
        :param event_type: Type of event ('data_transmission', 'calculation', etc.).
        :param kwargs: Additional data for the event.
        """
        self.events.append({"time": time, "type": event_type, **kwargs})
        self.events.sort(key=lambda e: e["time"])  # Keep events sorted by time

    def get_next_event(self):
        """
        Get the next event in the timeline (earliest by time).
        """
        if not self.events:
            return None
        return self.events.pop(0)
