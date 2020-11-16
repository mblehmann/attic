from collections import defaultdict


class EventBroker:
    """
    Event broker of the system. Registers the subscriptions and triggers the callback when the event happens
    """

    def __init__(self):
        """
        The subscriptions register callbacks to tuple of object, event
        """
        self._subscriptions = defaultdict(list)

    def subscribe(self, obj, event, callback):
        """
        Registers a callback to a tuple object, event

        :param obj: Object that triggered the event
        :param event: Triggered event
        :param callback: Registered callback
        :return: empty
        """
        self._subscriptions[(obj, event)].append(callback)

    def unsubscribe(self, obj, event, callback):
        """
        Unregisters a callback from a tuple object, event

        :param obj: Object that triggered the event
        :param event: Triggered event
        :param callback: Registered callback
        :return: empty
        """
        self._subscriptions[(obj, event)].remove(callback)

    def remove(self, obj, event):
        """
        Removes all callbacks related to the tuple object, event

        :param obj: Object that triggered the event
        :param event: Triggered event
        :return: empty
        """
        del self._subscriptions[(obj, event)]

    def trigger(self, obj, event, **kwargs):
        """
        Triggers the callbacks of the tuple object, event

        :param obj: Object that triggered the event
        :param event: Triggered event
        :param kwargs: Keyword arguments. They are checked by each callback
        :return: empty
        """
        for callback in self._subscriptions[(obj, event)]:
            callback(**kwargs)


broker = EventBroker()
