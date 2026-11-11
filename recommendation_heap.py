class MaxHeap:
    """Binary max heap for (recommendation_score, ISBN)."""
    def __init__(self): self.a=[]
    def __len__(self): return len(self.a)
    def push(self,x):
        self.a.append(x); i=len(self.a)-1
        while i:
            p=(i-1)//2
            if self.a[p]>=self.a[i]: break
            self.a[p],self.a[i]=self.a[i],self.a[p]; i=p
    def pop(self):
        if not self.a: return None
        if len(self.a)==1: return self.a.pop()
        top=self.a[0]; self.a[0]=self.a.pop(); i=0
        while True:
            l=2*i+1; r=l+1; m=i
            if l<len(self.a) and self.a[l]>self.a[m]: m=l
            if r<len(self.a) and self.a[r]>self.a[m]: m=r
            if m==i: break
            self.a[i],self.a[m]=self.a[m],self.a[i]; i=m
        return top
