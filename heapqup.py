from math import log, trunc
from itertools import count
import Queue as q

class heapitem:
    
    def __init__(self, k, v, c):
        self.c = c
        self.k = k
        self.v = v
        
    def heapvalue(self):
        if self.v is None:
            return self.k
        else:
            return self.v
        
class heapqup:

    __counter = count()

    def __heapord(self, pos1, pos2):
        "Returns True if item at pos1 should come before (be a parent of) item at pos2 in the heap ordering"
        item1 = self.__heapitems[pos1]
        item2 = self.__heapitems[pos2]
        ord1 = self.key(item1.heapvalue())
        ord2 = self.key(item2.heapvalue())
        
        # XOR reverse with the less-than ordering on the keyed heapvalues
        # break ties by having older items first
        if (ord1 < ord2) != self.reverse:
            return True
        elif (ord1 > ord2) != self.reverse:
            return False
        else:
            return item1.c < item2.c
            
    def __init__(self, src=None, key=lambda x: x, reverse=False):
        assert hasattr(key, '__call__')
        self.key = key
        self.reverse = reverse
        self.__positions = dict()
        self.__heapitems = list()
        
        if isinstance(src, dict):
            for k, v in src.items():
                self.__positions[k] = len(self.__heapitems)
                self.__heapitems.append(heapitem(k, v, next(self.__counter)))
        else:
            try:
                it = iter(src)
                for item in it:
                    if item not in self.__positions:
                        self.__positions[item] = len(self.__heapitems)
                        self.__heapitems.append(heapitem(item, None, next(self.__counter)))
            
            except TypeError:
                pass
                
        self.__heapify()
                
    def __heapify(self):
        num = len(self.__heapitems)
        
        if num < 2:
            return
        
        for level in range(trunc(log(num, 2))-1, -1, -1):
            for index in range( (2**level)-1, (2**(level+1))-1, 1):
                self.__heap_topdown(index)
        
    def __heap_topdown(self, pos):
        b = pos * 2 + 1
        if b >= len(self.__heapitems):
            return False
            
        ordered = self.__heapord(pos, b)

        if (b+1) >= len(self.__heapitems):
            if not ordered:
                self.__swap(pos, b)
                return True
            else:
                return False
        
        if ordered:
            ordered = self.__heapord(pos, b+1)
                
        if not ordered: # one of the children needs to become parent
            if self.__heapord(b, b+1):  # left child should be on top; swap parent with left child
                self.__swap(pos, b)
                self.__heap_topdown(b)
                return True
            else:   # right child should be on top; swap parent with right child
                self.__swap(pos, b+1)
                self.__heap_topdown(b+1)
                return True
        else:
            return False
        
    def __heap_bottomup(self, pos):
        a = (pos-1)//2
        if a >= 0:
            if not self.__heapord(a, pos):
                self.__swap(pos, a)
                self.__heap_bottomup(a)
                return True
        return False
                    
    def __swap(self, p1, p2):
        self.__heapitems[p1], self.__heapitems[p2] = self.__heapitems[p2], self.__heapitems[p1]
        self.__fixkeypos(p1)
        self.__fixkeypos(p2)
        
    def __fixkeypos(self, pos):
        self.__positions[self.__heapitems[pos].k] = pos        
        
    def offer(self, k, v=None):
        if k in self.__positions:
            # This is an update
            pos = self.__positions[k]
            if v != self.__heapitems[pos].v:
                self.__heapitems[pos] = heapitem(k, v, next(self.__counter))
                if not self.__heap_bottomup(pos):
                    self.__heap_topdown(pos)
                    
        else:
            # This is an add
            pos = len(self.__heapitems)
            self.__positions[k] = pos
            self.__heapitems.append(heapitem(k, v, next(self.__counter)))
            self.__heap_bottomup(pos)
    
    def poll(self, value=False):
        r = self.peek(value)

        del self.__positions[self.__heapitems[0].k]
        if len(self.__heapitems) > 1:
            self.__heapitems[0] = self.__heapitems.pop()
            self.__fixkeypos(0)
            self.__heap_topdown(0)
        else:
            del self.__heapitems[0]
                    
        return r
        
    def peek(self, value=False):
        if len(self.__heapitems) <= 0:
            raise IndexError, "heap is empty"
    
        if value:
            r = (self.__heapitems[0].k, self.__heapitems[0].heapvalue())
        else:
            r = self.__heapitems[0].k
            
        return r
        
    def update(self, k, v):
        self.offer(k, v)
    
    def get_list(self):
        return [(hpi.k, hpi.v) for hpi in self.__heapitems]

    def peek_all(self):
        '''
        return a list of keys whose values are maximum in the heap
        '''
        root = self.__heapitems[0]
        return_list = [root.k]
        max_val = root.v
        queue = q.Queue()
        queue.put((root.k, self.__positions[root.k]))
        while not queue.empty():
            self_pos = queue.get()[1]
            left_child_pos = 2*self_pos + 1
            right_child_pos = left_child_pos + 1
            if left_child_pos < len(self.__heapitems):
                left_child = self.__heapitems[left_child_pos]
                left_child_val = left_child.v
                if left_child_val == max_val:
                    return_list.append(left_child.k)
                    queue.put((left_child.k, self.__positions[left_child.k]))
            if right_child_pos < len(self.__heapitems):
                right_child = self.__heapitems[right_child_pos]
                right_child_val = right_child.v
                if right_child_val == max_val:
                    return_list.append(right_child.k)
                    queue.put((right_child.k, self.__positions[right_child.k]))
        return return_list

    def remove(self, k):
        '''
        remove the heapitem that matches the given key
        '''
        pos_1 = self.__positions[k]
        if pos_1 != len(self.__heapitems) - 1:
            pos_2 = len(self.__heapitems) - 1
            self.__swap(pos_1, pos_2)
            hp_item = self.__heapitems[pos_1]
            self.update(hp_item.k, hp_item.v)
        del self.__positions[k]
        del self.__heapitems[len(self.__heapitems) - 1] 


    def __len__(self):
        return len(self.__heapitems)
        
    def debug(self):
        assert len(self.__positions) == len(self.__heapitems)
        assert len(self.__positions.values()) == len(self.__positions)
        assert all(map(lambda x: 0 <= x < len(self.__heapitems), self.__positions.values()))
        return [(item.k, item.v, item.c, item==self.__heapitems[self.__positions[item.k]]) for item in self.__heapitems]