class Node:
    def __init__(self,k,v):
        self.key=k.casefold(); self.value=v; self.left=self.right=None; self.height=1
class AVLTree:
    """Self-balancing AVL tree for exact title lookup."""
    def __init__(self): self.root=None
    def h(self,n): return n.height if n else 0
    def upd(self,n): n.height=1+max(self.h(n.left),self.h(n.right))
    def bal(self,n): return self.h(n.left)-self.h(n.right)
    def rr(self,y):
        x=y.left; t=x.right; x.right=y; y.left=t; self.upd(y); self.upd(x); return x
    def rl(self,x):
        y=x.right; t=y.left; y.left=x; x.right=t; self.upd(x); self.upd(y); return y
    def insert(self,k,v): self.root=self._ins(self.root,k,v)
    def _ins(self,n,k,v):
        if not n: return Node(k,v)
        key=k.casefold()
        if key<n.key: n.left=self._ins(n.left,k,v)
        elif key>n.key: n.right=self._ins(n.right,k,v)
        else: n.value=v; return n
        self.upd(n); b=self.bal(n)
        if b>1 and key<n.left.key: return self.rr(n)
        if b<-1 and key>n.right.key: return self.rl(n)
        if b>1 and key>n.left.key: n.left=self.rl(n.left); return self.rr(n)
        if b<-1 and key<n.right.key: n.right=self.rr(n.right); return self.rl(n)
        return n
    def search(self,k):
        n=self.root; k=k.casefold()
        while n:
            if k==n.key: return n.value
            n=n.left if k<n.key else n.right
        return None
