# Library Book Search and Recommendation System (Tkinter)

## Run
Install dependencies:
```bash
python -m pip install matplotlib
```
Tkinter is normally included with Windows Python. Run from this folder:
```bash
python dashboard.py
```

## Features
Dashboard, catalog sorting, add/search/update/delete, graph-based recommendations,
borrow/return, transaction history, and performance benchmarking.

## DSA
Hash table with separate chaining (ISBN lookup), AVL tree (exact title lookup),
adjacency-list graph + BFS (related books), binary max heap (recommendation ranking),
and merge sort (catalog sorting).

Sample books are created on first launch. Records persist in `data/books.json`
and `data/transactions.json`. Recommendation scoring is a heuristic, not ML.
