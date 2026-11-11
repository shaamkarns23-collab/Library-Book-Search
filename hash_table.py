class HashTable:
    """Separate-chaining hash table for ISBN lookup."""
    def __init__(self, capacity=101):
        self.capacity=capacity; self.buckets=[[] for _ in range(capacity)]; self.size=0
    def _i(self,k): return hash(str(k)) % self.capacity
    def put(self,k,v):
        b=self.buckets[self._i(k)]
        for i,(key,_) in enumerate(b):
            if key==k: b[i]=(k,v); return
        b.append((k,v)); self.size+=1
    def get(self,k):
        for key,v in self.buckets[self._i(k)]:
            if key==k: return v
        return None
    def remove(self,k):
        b=self.buckets[self._i(k)]
        for i,(key,_) in enumerate(b):
            if key==k: del b[i]; self.size-=1; return True
        return False
