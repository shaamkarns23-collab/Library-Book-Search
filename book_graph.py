from collections import defaultdict, deque
class BookGraph:
    """Undirected adjacency-list graph. Books connect by author or category."""
    def __init__(self): self.adj=defaultdict(set)
    def add_vertex(self,x): self.adj[x]
    def add_edge(self,a,b):
        if a!=b: self.adj[a].add(b); self.adj[b].add(a)
    def bfs(self,start,max_depth=3):
        if start not in self.adj: return []
        seen={start}; q=deque([(start,0)]); out=[]
        while q:
            u,d=q.popleft()
            if d==max_depth: continue
            for v in self.adj[u]:
                if v not in seen: seen.add(v); out.append(v); q.append((v,d+1))
        return out
