'''
Based on Priority Dict, a tool created by Matteo Dell'Amico
on ActiveState Code. URL: http://code.activestate.com/recipes/
522995-priority-dict-a-priority-queue-with-updatable-prio/.

(c) Yuxin David Huang '16, Colgate University
All Rights Reserved.
'''

from heapq import heapify, heappush, heappop

class updatable_min_PQ(dict):
    '''
    An updatable priority queue implemented using a dictionary.

    Keys of the dictionary are items to be put into the queue,
    and values are their respective priorities. All dictionary
    methods work as expected.

    The advantage over a standard heapq-based priority queue is
    that priorities of items can be efficiently updated (amortized
    O(1)) using code as "dict[item] = new_priority".

    The "dequeue" method can be used to return the object with
    highest priority. The object will also be removed in the process.

    The "poll" method is used to look at (return but not remove) the
    object with the highest priority.
    '''

    def __init__(self, *args, **kwargs):
        super(updatable_min_PQ, self).__init__(*args, **kwargs)
        self._rebuild_heap()

    def _rebuild_heap(self):
        self._heap = [(v, k) for k, v in self.iteritems()]
        heapify(self._heap)

    def poll(self):
        '''
        Return the item with the highest priority.
        '''

        heap = self._heap
        v, k = heap[0]
        while k not in self or self[k] != v:
            heappop(heap)
            v, k = heap[0]
        return k

    def dequeue(self):
        '''
        Return the item with the highest priority and removes it.
        '''

        heap = self._heap
        v, k = heappop(heap)
        while k not in self or self[k] != v:
            v, k = heappop(heap)
        del self[k]
        return k

    def __setitem__(self, key, val):
        '''
        The priority values are put in negative because the heapq
        module uses a min-heap. This will make sure that objects
        with higher priorities (therefore more negative and
        "smaller") will be returned before ones with lower priorities.
        '''

        super(updatable_min_PQ, self).__setitem__(key, val)

        if len(self._heap) < 2 * len(self):
            heappush(self._heap, (val, key))
        else:
            self._rebuild_heap()

    def setdefault(self, key, val):
        if key not in self:
            self[key] = val
            return val
        return self[key]

    def update(self, *args, **kwargs):

        super(updatable_min_PQ, self).update(*args, **kwargs)
        self._rebuild_heap()
