import json
from pathlib import Path
from datetime import datetime
from book import Book
from hash_table import HashTable
from avl_tree import AVLTree
from book_graph import BookGraph
from recommendation_heap import MaxHeap
from merge_sort import merge_sort

class LibraryManager:
    def __init__(self,data_dir="data"):
        self.path=Path(data_dir); self.path.mkdir(parents=True,exist_ok=True)
        self.bfile=self.path/"books.json"; self.tfile=self.path/"transactions.json"
        if self.bfile.exists():
            self.books={b.isbn:b for b in map(Book.from_dict,json.loads(self.bfile.read_text(encoding="utf-8")))}
        else:
            sample=[
             Book("9780132350884","Clean Code","Robert C. Martin","Software Engineering",2008,4.7,4,4),
             Book("9780201633610","Design Patterns","Erich Gamma","Software Engineering",1994,4.6,3,3),
             Book("9780131103627","The C Programming Language","Brian Kernighan","Programming",1988,4.5,3,3),
             Book("9780262033848","Introduction to Algorithms","Thomas Cormen","Algorithms",2022,4.8,2,2),
             Book("9781492056355","Fluent Python","Luciano Ramalho","Programming",2022,4.6,2,2),
             Book("9780134685991","Effective Java","Joshua Bloch","Programming",2018,4.7,2,2),
             Book("9780262046305","Machine Learning","Ethem Alpaydin","Artificial Intelligence",2020,4.2,2,2),
             Book("9780135957059","Artificial Intelligence: A Modern Approach","Stuart Russell","Artificial Intelligence",2021,4.6,2,2),
             Book("9780262033849","Introduction to Information Retrieval","Christopher Manning","Data Science",2008,4.3,2,2),
             Book("9781491912058","Python for Data Analysis","Wes McKinney","Data Science",2022,4.5,3,3)]
            self.books={b.isbn:b for b in sample}; self._save_books()
        self.transactions=json.loads(self.tfile.read_text(encoding="utf-8")) if self.tfile.exists() else []
        self._save_transactions(); self._indexes()
    def _save_books(self): self.bfile.write_text(json.dumps([b.to_dict() for b in self.books.values()],indent=2),encoding="utf-8")
    def _save_transactions(self): self.tfile.write_text(json.dumps(self.transactions,indent=2),encoding="utf-8")
    def _indexes(self):
        self.isbn=HashTable(); self.title=AVLTree(); self.graph=BookGraph()
        vals=list(self.books.values())
        for b in vals: self.isbn.put(b.isbn,b); self.title.insert(b.title,b); self.graph.add_vertex(b.isbn)
        for i,a in enumerate(vals):
            for b in vals[i+1:]:
                if a.author.casefold()==b.author.casefold() or a.category.casefold()==b.category.casefold():
                    self.graph.add_edge(a.isbn,b.isbn)
    def _record(self,action,b,borrower=""):
        self.transactions.append({"action":action,"isbn":b.isbn,"title":b.title,"borrower":borrower,"timestamp":datetime.now().isoformat(timespec="seconds")})
        self._save_transactions()
    def add_book(self,b):
        if not b.isbn or not b.title.strip(): raise ValueError("ISBN and title are required.")
        if b.isbn in self.books: raise ValueError("ISBN already exists.")
        if b.total_copies<1: raise ValueError("Total copies must be at least 1.")
        self.books[b.isbn]=b; self._save_books(); self._indexes(); self._record("ADDED",b)
    def update_book(self,isbn,**changes):
        b=self.isbn.get(isbn)
        if not b: raise ValueError("Book not found.")
        for k,v in changes.items():
            if v is not None and k in {"title","author","category","year","rating"}: setattr(b,k,v)
        if not 0<=b.rating<=5: raise ValueError("Rating must be between 0 and 5.")
        self._save_books(); self._indexes(); self._record("UPDATED",b); return b
    def delete_book(self,isbn):
        b=self.isbn.get(isbn)
        if not b: raise ValueError("Book not found.")
        if b.available_copies!=b.total_copies: raise ValueError("Return all copies before deleting.")
        del self.books[isbn]; self._save_books(); self._indexes(); self._record("DELETED",b)
    def search(self,q):
        q=q.casefold().strip()
        return [b for b in self.books.values() if q in b.isbn.casefold() or q in b.title.casefold() or q in b.author.casefold() or q in b.category.casefold()]
    def all_books(self,sort="title"):
        keys={"title":lambda b:b.title.casefold(),"author":lambda b:b.author.casefold(),"year":lambda b:b.year,"rating":lambda b:b.rating,"category":lambda b:b.category.casefold()}
        return merge_sort(list(self.books.values()),key=keys.get(sort,keys["title"]))
    def borrow_book(self,isbn,borrower):
        b=self.isbn.get(isbn); borrower=borrower.strip()
        if not b: raise ValueError("Book not found.")
        if not borrower: raise ValueError("Borrower name is required.")
        if b.available_copies<1: raise ValueError("No available copies.")
        b.available_copies-=1; self._save_books(); self._record("BORROWED",b,borrower)
    def return_book(self,isbn,borrower):
        b=self.isbn.get(isbn); borrower=borrower.strip()
        if not b: raise ValueError("Book not found.")
        count=0
        for t in self.transactions:
            if t["isbn"]==isbn and t.get("borrower","").casefold()==borrower.casefold():
                if t["action"]=="BORROWED": count+=1
                elif t["action"]=="RETURNED": count-=1
        if count<=0: raise ValueError("No outstanding loan for this borrower.")
        if b.available_copies>=b.total_copies: raise ValueError("All copies already available.")
        b.available_copies+=1; self._save_books(); self._record("RETURNED",b,borrower)
    def recommend(self,isbn,limit=5):
        source=self.isbn.get(isbn)
        if not source: return []
        heap=MaxHeap()
        for key in self.graph.bfs(isbn):
            b=self.isbn.get(key)
            if b:
                score=(5 if b.category.casefold()==source.category.casefold() else 0)+(4 if b.author.casefold()==source.author.casefold() else 0)+b.rating+(1 if b.available_copies else 0)
                heap.push((score,b.isbn))
        out=[]
        while len(heap) and len(out)<limit: out.append(self.isbn.get(heap.pop()[1]))
        return out
