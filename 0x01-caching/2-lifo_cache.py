#!/usr/bin/python3
""" LIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class that inherits from BaseCaching
    Last-In-First-Out caching system
    """

    def __init__(self):
        """ Initialize LIFOCache
        """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """ Add an item in the cache
        If cache exceeds MAX_ITEMS, discard the last item (LIFO)
        """
        if key is None or item is None:
            return

        # Update key if it exists or add it if it doesn't
        if key in self.cache_data:
            # Remove key from stack since we're updating it
            self.stack.remove(key)

        # Add to cache and stack
        self.cache_data[key] = item
        self.stack.append(key)

        # If cache exceeds MAX_ITEMS, discard last item (LIFO)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Pop the last added key before the current one
            last_key = self.stack.pop(-2)
            del self.cache_data[last_key]
            print("DISCARD:", last_key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
