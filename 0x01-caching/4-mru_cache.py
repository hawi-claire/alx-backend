#!/usr/bin/python3
""" MRUCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class that inherits from BaseCaching
    Most Recently Used caching system
    """

    def __init__(self):
        """ Initialize MRUCache
        """
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """ Add an item in the cache
        If cache exceeds MAX_ITEMS, discard the most recently used item (MRU)
        """
        if key is None or item is None:
            return

        # If key exists, remove it from usage_order to update position
        if key in self.cache_data:
            self.usage_order.remove(key)

        # Add key to cache and update usage order
        self.cache_data[key] = item
        self.usage_order.append(key)

        # If cache exceeds MAX_ITEMS, discard most recently used item
        # (which is the second most recent, since the current key is the most recent)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Remove the most recently used item before the current one
            mru_key = self.usage_order[-2]
            self.usage_order.remove(mru_key)
            del self.cache_data[mru_key]
            print("DISCARD:", mru_key)

    def get(self, key):
        """ Get an item by key
        Updates the usage order to mark this key as most recently used
        """
        if key is None or key not in self.cache_data:
            return None

        # Update usage order by moving key to the end (most recently used)
        self.usage_order.remove(key)
        self.usage_order.append(key)

        return self.cache_data[key]
