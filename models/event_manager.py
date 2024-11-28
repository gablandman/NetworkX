class EventManager:
    """
    Manages the list of events during the simulation.
    """
    def __init__(self):
        self.events = []

    def add_event(self, time, event_type, **kwargs):
        """
        Add a new event to the list.

        :param time: Timestamp of the event.
        :param event_type: Type of event ('data_transmission', 'start_calculation', 'end_calculation').
        :param kwargs: Additional data for the event.
        """
        self.events.append({"time": time, "type": event_type, **kwargs})

    def get_events(self):
        """
        Get the list of events sorted by time.
        """
        return sorted(self.events, key=lambda e: e["time"])
