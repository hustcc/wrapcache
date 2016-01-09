# -*- coding: utf-8 -*-
# The cache is implemented using a combination of a python dictionary (hash
# table) and a circular doubly linked list. Items in the cache are stored in
# nodes. These nodes make up the linked list. The list is used to efficiently
# maintain the order that the items have been used in. The front or head of
# the list contains the most recently used item, the tail of the list
# contains the least recently used item. When an item is used it can easily
# (in a constant amount of time) be moved to the front of the list, thus
# updating its position in the ordering. These nodes are also placed in the
# hash table under their associated key. The hash table allows efficient
# lookup of values by key.

# Class for the node objects.
class _dlnode(object):
    def __init__(self):
        self.empty = True


class LruDB(object):
    def __init__(self, size):

        # Create an empty hash table.
        self.table = {}

        # Initialize the doubly linked list with one empty node. This is an
        # invariant. The cache size must always be greater than zero. Each
        # node has a 'prev' and 'next' variable to hold the node that comes
        # before it and after it respectively. Initially the two variables
        # each point to the head node itself, creating a circular doubly
        # linked list of size one. Then the size() method is used to adjust
        # the list to the desired size.

        self.head = _dlnode()
        self.head.next = self.head
        self.head.prev = self.head

        self.listSize = 1

        # Adjust the size
        self.size(size)
        
        #status var
        self.hits = 0 
        self.miss = 0
        self.remove = 0

    def __len__(self):
        return len(self.table)

    def clear(self):
        for node in self.dli():
            node.empty = True
            node.key = None
            node.value = None

        self.table.clear()
        
        # status var
        self.hits = 0 
        self.miss = 0
        self.remove = 0

    def __contains__(self, key):
        return key in self.table

    # Looks up a value in the cache without affecting cache order.
    def peek(self, key):
        # Look up the node
        node = self.table[key]
        return node.value


    def __getitem__(self, key):
        # Look up the node
        try:
            node = self.table[key]
            self.hits += 1
        except KeyError:
            self.miss += 1
            raise KeyError

        # Update the list ordering. Move this node so that is directly
        # proceeds the head node. Then set the 'head' variable to it. This
        # makes it the new head of the list.
        self.mtf(node)
        self.head = node

        # Return the value.
        return node.value

    def get(self, key, default = None):
        """Get an item - return default (None) if not present"""
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        # First, see if any value is stored under 'key' in the cache already.
        # If so we are going to replace that value with the new one.
        if key in self.table:

            # Lookup the node
            node = self.table[key]

            # Replace the value.
            node.value = value

            # Update the list ordering.
            self.mtf(node)
            self.head = node

            return

        # Ok, no value is currently stored under 'key' in the cache. We need
        # to choose a node to place the new item in. There are two cases. If
        # the cache is full some item will have to be pushed out of the
        # cache. We want to choose the node with the least recently used
        # item. This is the node at the tail of the list. If the cache is not
        # full we want to choose a node that is empty. Because of the way the
        # list is managed, the empty nodes are always together at the tail
        # end of the list. Thus, in either case, by chooseing the node at the
        # tail of the list our conditions are satisfied.

        # Since the list is circular, the tail node directly preceeds the
        # 'head' node.
        node = self.head.prev

        # If the node already contains something we need to remove the old
        # key from the dictionary.
        if not node.empty:
            del self[node.key]

        # Place the new key and value in the node
        node.empty = False
        node.key = key
        node.value = value

        # Add the node to the dictionary under the new key.
        self.table[key] = node

        # We need to move the node to the head of the list. The node is the
        # tail node, so it directly preceeds the head node due to the list
        # being circular. Therefore, the ordering is already correct, we just
        # need to adjust the 'head' variable.
        self.head = node


    def __delitem__(self, key):
        # Lookup the node, then remove it from the hash table.
        node = self.table[key]
        del self.table[key]

        node.empty = True

        # Not strictly necessary.
        node.key = None
        node.value = None

        # Because this node is now empty we want to reuse it before any
        # non-empty node. To do that we want to move it to the tail of the
        # list. We move it so that it directly preceeds the 'head' node. This
        # makes it the tail node. The 'head' is then adjusted. This
        # adjustment ensures correctness even for the case where the 'node'
        # is the 'head' node.
        self.mtf(node)
        self.head = node.next
        
        self.remove += 1

    def __iter__(self):

        # Return an iterator that returns the keys in the cache in order from
        # the most recently to least recently used. Does not modify the cache
        # order.
        for node in self.dli():
            yield node.key

    def items(self):

        # Return an iterator that returns the (key, value) pairs in the cache
        # in order from the most recently to least recently used. Does not
        # modify the cache order.
        for node in self.dli():
            yield (node.key, node.value)

    def keys(self):

        # Return an iterator that returns the keys in the cache in order from
        # the most recently to least recently used. Does not modify the cache
        # order.
        for node in self.dli():
            yield node.key

    def values(self):

        # Return an iterator that returns the values in the cache in order
        # from the most recently to least recently used. Does not modify the
        # cache order.
        for node in self.dli():
            yield node.value

    def size(self, size = None):

        if size is not None:
            assert size > 0
            if size > self.listSize:
                self.addTailNode(size - self.listSize)
            elif size < self.listSize:
                self.removeTailNode(self.listSize - size)

        return self.listSize

    # Increases the size of the cache by inserting n empty nodes at the tail
    # of the list.
    def addTailNode(self, n):
        for _ in range(n):
            node = _dlnode()
            node.next = self.head
            node.prev = self.head.prev

            self.head.prev.next = node
            self.head.prev = node

        self.listSize += n

    # Decreases the size of the list by removing n nodes from the tail of the
    # list.
    def removeTailNode(self, n):
        assert self.listSize > n
        for _ in range(n):
            node = self.head.prev
            if not node.empty:
                del self[node.key]

            # Splice the tail node out of the list
            self.head.prev = node.prev
            node.prev.next = self.head

            # The next four lines are not strictly necessary.
            node.prev = None
            node.next = None

            node.key = None
            node.value = None

        self.listSize -= n


    # This method adjusts the ordering of the doubly linked list so that
    # 'node' directly precedes the 'head' node. Because of the order of
    # operations, if 'node' already directly precedes the 'head' node or if
    # 'node' is the 'head' node the order of the list will be unchanged.
    def mtf(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = self.head.prev
        node.next = self.head.prev.next

        node.next.prev = node
        node.prev.next = node

    # This method returns an iterator that iterates over the non-empty nodes
    # in the doubly linked list in order from the most recently to the least
    # recently used.
    def dli(self):
        node = self.head
        for _ in range(len(self.table)):
            yield node
            node = node.next
    
    
    
    def status(self):
        used = 0
        for node in self.dli():
            if not node.empty:
                used += 1
        used_status = """
Single process cache used status:
    max:%s
    used:%s
    miss:%s
    hits:%s
    remove:%s
""" % (self.listSize, used, self.miss, self.hits, self.remove)
        print (used_status)
        
    
if __name__ == '__main__':
    import unittest, time, pprint

    class TestLruCase(unittest.TestCase):
        def setUp(self):
            self.test_class = LruDB(2)
        def tearDown(self):
            pass
        
        def test_lru_db(self):
            key1 = 'test_key_1'
            value1 = 'test_value_1'
            key2 = 'test_key_2'
            value2 = 'test_value_2'
            key3 = 'test_key_3'
            value3 = 'test_value_3'
            
            self.assertRaises(KeyError, self.test_class.__getitem__, key1)
            
            self.test_class[key1] = value1
            self.assertEqual(self.test_class[key1], value1)
            
            self.test_class.clear()
            self.assertRaises(KeyError, self.test_class.__getitem__, key1)
            
            self.test_class[key1] = value1
            self.test_class[key2] = value2
            self.test_class[key3] = value3
            
            x_array = []
            for x in self.test_class.keys():
                x_array.append(x)
            
            self.assertEqual(x_array, ['test_key_3', 'test_key_2'])
            
            self.test_class[key2]
            x_array = []
            for x in self.test_class.keys():
                x_array.append(x)
            
            self.assertEqual(x_array, ['test_key_2', 'test_key_3'])
            
            self.test_class.peek(key3)
            x_array = []
            for x in self.test_class.keys():
                x_array.append(x)
            
            self.assertEqual(x_array, ['test_key_2', 'test_key_3'])
            
    unittest.main()