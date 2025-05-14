#!/usr/bin/python3
""" FIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class that inherits from BaseCaching
    First-In-First-Out caching system
    """

    def __init__(self):
        """ Initialize FIFOCache
        """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache
        If cache exceeds MAX_ITEMS, discard the first item (FIFO)
        """
        if key is None or item is None:
            return

        # Update key if it exists or add it if it doesn't
        if key in self.cache_data:
            # Remove key from queue since we're updating it
            self.queue.remove(key)
        
        # Add to cache and queue
        self.cache_data[key] = item
        self.queue.append(key)

        # If cache exceeds MAX_ITEMS, discard first item (FIFO)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = self.queue.pop(0)
            del self.cache_data[first_key]
            print("DISCARD:", first_key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
