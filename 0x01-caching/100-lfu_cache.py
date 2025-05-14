#!/usr/bin/python3
""" LFUCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching
    Least Frequently Used caching system
    If multiple items have the same frequency, use LRU algorithm as a tiebreaker
    """

    def __init__(self):
        """ Initialize LFUCache
        """
        super().__init__()
        # Track frequency of each key
        self.frequencies = {}
        # Track usage recency for LRU tiebreaking
        self.usage_order = []

    def put(self, key, item):
        """ Add an item in the cache
        If cache exceeds MAX_ITEMS, discard the least frequently used item
        If multiple items have the same frequency, discard the least recently used
        """
        if key is None or item is None:
            return

        # Case 1: Key exists in cache (update operation)
        if key in self.cache_data:
            # Update the cache value
            self.cache_data[key] = item
            # Increment frequency
            self.frequencies[key] += 1
            # Update usage recency
            self._update_usage_recency(key)
            return

        # Case 2: Cache is full and need to evict
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            self._evict_lfu_item()

        # Case 3: Add the new key-item pair
        self.cache_data[key] = item
        # Initialize frequency to 1
        self.frequencies[key] = 1
        # Add to usage order for LRU tracking
        self.usage_order.append(key)

    def get(self, key):
        """ Get an item by key
        Updates the frequency and recency of the accessed key
        """
        if key is None or key not in self.cache_data:
            return None

        # Increment frequency because the key was accessed
        self.frequencies[key] += 1
        # Update usage recency
        self._update_usage_recency(key)

        return self.cache_data[key]

    def _update_usage_recency(self, key):
        """ Update the usage recency of a key (LRU tracking)
        """
        if key in self.usage_order:
            self.usage_order.remove(key)
        self.usage_order.append(key)

    def _evict_lfu_item(self):
        """ Evict the least frequently used item
        If tie, evict the least recently used item among them
        """
        # Find the minimum frequency
        min_freq = min(self.frequencies.values())
        
        # Get all keys with the minimum frequency
        min_freq_keys = [k for k, v in self.frequencies.items() if v == min_freq]
        
        # If there's only one key with minimum frequency, discard it
        if len(min_freq_keys) == 1:
            lfu_key = min_freq_keys[0]
        else:
            # Multiple keys with same frequency, use LRU to break the tie
            # Find the least recently used key among the min frequency keys
            for key in self.usage_order:
                if key in min_freq_keys:
                    lfu_key = key
                    break
        
        # Remove the key from all tracking structures
        del self.cache_data[lfu_key]
        del self.frequencies[lfu_key]
        self.usage_order.remove(lfu_key)
        
        print("DISCARD:", lfu_key)
