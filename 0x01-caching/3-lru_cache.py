#!/usr/bin/python3
""" LRUCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class that inherits from BaseCaching
    Least Recently Used caching system
    """

    def __init__(self):
        """ Initialize LRUCache
        """
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """ Add an item in the cache
        If cache exceeds MAX_ITEMS, discard the least recently used item (LRU)
        """
        if key is None or item is None:
            return

        # If key exists, remove it from usage_order to update position
        if key in self.cache_data:
            self.usage_order.remove(key)

        # Add key to cache and update usage order
        self.cache_data[key] = item
        self.usage_order.append(key)

        # If cache exceeds MAX_ITEMS, discard least recently used item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lru_key = self.usage_order.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD:", lru_key)

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
