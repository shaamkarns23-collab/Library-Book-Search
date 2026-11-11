import random,time
from hash_table import HashTable
from avl_tree import AVLTree
from merge_sort import merge_sort
def run_benchmarks(sizes=(100,500,1000,5000,10000),repeats=5):
    out={k:[] for k in ["size","hash_ms","linear_ms","avl_ms","linear_title_ms","merge_ms","builtin_ms"]}
    def timeit(fn):
        t=time.perf_counter()
        for _ in range(repeats): fn()
        return (time.perf_counter()-t)*1000/repeats
    for n in sizes:
        data=[(f"ISBN{i:08d}",f"Book {i:08d}") for i in range(n)]
        h=HashTable(); a=AVLTree()
        for isbn,title in data: h.put(isbn,title); a.insert(title,isbn)
        target=data[-1]; shuffled=data[:]; random.Random(42).shuffle(shuffled)
        out["size"].append(n)
        out["hash_ms"].append(timeit(lambda:h.get(target[0])))
        out["linear_ms"].append(timeit(lambda:next((x for x in data if x[0]==target[0]),None)))
        out["avl_ms"].append(timeit(lambda:a.search(target[1])))
        out["linear_title_ms"].append(timeit(lambda:next((x for x in data if x[1]==target[1]),None)))
        out["merge_ms"].append(timeit(lambda:merge_sort(shuffled,key=lambda x:x[1])))
        out["builtin_ms"].append(timeit(lambda:sorted(shuffled,key=lambda x:x[1])))
    return out
