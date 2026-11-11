import tkinter as tk
from tkinter import ttk,messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from library_manager import LibraryManager
from book import Book
from performance_analyzer import run_benchmarks

class LibraryApp:
 def __init__(self,root):
  self.root=root; root.title("Library Book Search & Recommendation System"); root.geometry("1250x760"); root.minsize(1000,620)
  self.lib=LibraryManager(); self.bg="#f1f5f9"; self.navy="#172554"; root.configure(bg=self.bg); self.styles(); self.shell(); self.dashboard()
 def styles(self):
  s=ttk.Style()
  try:s.theme_use("clam")
  except tk.TclError:pass
  s.configure("Treeview",rowheight=28,font=("Segoe UI",10)); s.configure("Treeview.Heading",font=("Segoe UI",10,"bold"),background="#dbeafe")
  s.configure("Side.TButton",background=self.navy,foreground="white",anchor="w",padding=(12,10))
  s.map("Side.TButton",background=[("active","#1e40af")])
  s.configure("Title.TLabel",font=("Segoe UI",21,"bold"),foreground=self.navy,background=self.bg)
 def shell(self):
  side=tk.Frame(self.root,bg=self.navy,width=230); side.pack(side="left",fill="y"); side.pack_propagate(False)
  tk.Label(side,text="📚 LIBRARY",bg=self.navy,fg="white",font=("Segoe UI",19,"bold")).pack(anchor="w",padx=17,pady=(25,2))
  tk.Label(side,text="BOOK MANAGEMENT SYSTEM",bg=self.navy,fg="#bfdbfe",font=("Segoe UI",8,"bold")).pack(anchor="w",padx=19,pady=(0,20))
  pages=[("Dashboard",self.dashboard),("Book Catalog",self.catalog),("Add New Book",self.add),("Search Books",self.search),("Manage Books",self.manage),("Recommendations",self.recommend),("Borrow / Return",self.circulation),("Transaction History",self.history),("Performance Analysis",self.analytics)]
  for name,fn in pages: ttk.Button(side,text="  "+name,style="Side.TButton",command=fn).pack(fill="x",padx=9,pady=3)
  tk.Label(side,text="DATA STRUCTURES MINI PROJECT",bg=self.navy,fg="#93c5fd",font=("Segoe UI",8,"bold")).pack(side="bottom",pady=18)
  self.body=tk.Frame(self.root,bg=self.bg); self.body.pack(side="right",fill="both",expand=True,padx=25,pady=22)
 def clear(self):
  for w in self.body.winfo_children():w.destroy()
 def head(self,title,sub):
  ttk.Label(self.body,text=title,style="Title.TLabel").pack(anchor="w")
  tk.Label(self.body,text=sub,bg=self.bg,fg="#64748b").pack(anchor="w",pady=(3,15))
 def msg(self,s,err=False):(messagebox.showerror if err else messagebox.showinfo)("Library",s)
 def table(self,cols):
  f=tk.Frame(self.body,bg="white"); f.pack(fill="both",expand=True,pady=10); t=ttk.Treeview(f,columns=cols,show="headings")
  for c in cols:t.heading(c,text=c);t.column(c,width=125,minwidth=90)
  sy=ttk.Scrollbar(f,orient="vertical",command=t.yview); sx=ttk.Scrollbar(f,orient="horizontal",command=t.xview); t.configure(yscrollcommand=sy.set,xscrollcommand=sx.set)
  t.grid(row=0,column=0,sticky="nsew");sy.grid(row=0,column=1,sticky="ns");sx.grid(row=1,column=0,sticky="ew");f.rowconfigure(0,weight=1);f.columnconfigure(0,weight=1);return t
 def fill(self,t,books):
  t.delete(*t.get_children())
  for b in books:t.insert("","end",values=(b.isbn,b.title,b.author,b.category,b.year,f"{b.rating:.1f}",f"{b.available_copies}/{b.total_copies}"))
 def dashboard(self):
  self.clear();self.head("Dashboard","Library inventory and activity overview")
  row=tk.Frame(self.body,bg=self.bg);row.pack(fill="x",pady=(0,15))
  vals=[("Total Titles",len(self.lib.books)),("Available Copies",sum(b.available_copies for b in self.lib.books.values())),("Borrowed Copies",sum(b.total_copies-b.available_copies for b in self.lib.books.values())),("Transactions",len(self.lib.transactions))]
  for label,value in vals:
   c=tk.Frame(row,bg="white",padx=17,pady=14);c.pack(side="left",fill="x",expand=True,padx=(0,10))
   tk.Label(c,text=label,bg="white",fg="#64748b").pack(anchor="w");tk.Label(c,text=str(value),bg="white",fg=self.navy,font=("Segoe UI",22,"bold")).pack(anchor="w")
  f=tk.Frame(self.body,bg="white");f.pack(fill="both",expand=True);cats={}
  for b in self.lib.books.values():cats[b.category]=cats.get(b.category,0)+1
  fig,ax=plt.subplots(figsize=(8,4),dpi=100)
  if cats:ax.bar(list(cats),list(cats.values()));ax.set_title("Books by Category");ax.tick_params(axis="x",rotation=20)
  fig.tight_layout();can=FigureCanvasTkAgg(fig,master=f);can.draw();can.get_tk_widget().pack(fill="both",expand=True);plt.close(fig)
 def catalog(self):
  self.clear();self.head("Book Catalog","Browse and sort the collection");bar=tk.Frame(self.body,bg=self.bg);bar.pack(anchor="w")
  tk.Label(bar,text="Sort by",bg=self.bg).pack(side="left");s=ttk.Combobox(bar,values=["title","author","year","rating","category"],state="readonly",width=15);s.set("title");s.pack(side="left",padx=8)
  t=self.table(("ISBN","Title","Author","Category","Year","Rating","Copies"))
  def refresh(e=None):self.fill(t,self.lib.all_books(s.get()))
  s.bind("<<ComboboxSelected>>",refresh);refresh()
 def add(self):
  self.clear();self.head("Add New Book","Add a new title to inventory");f=tk.Frame(self.body,bg="white",padx=22,pady=18);f.pack(anchor="nw",fill="x")
  labels=["ISBN","Title","Author","Category","Year","Rating","Total Copies"];es={}
  for i,k in enumerate(labels):
   tk.Label(f,text=k,bg="white").grid(row=i,column=0,sticky="w",pady=5);es[k]=ttk.Entry(f,width=42);es[k].grid(row=i,column=1,padx=12,pady=5)
  for k,v in {"Year":"2025","Rating":"4.0","Total Copies":"1"}.items():es[k].insert(0,v)
  def save():
   try:
    n=int(es["Total Copies"].get());r=float(es["Rating"].get())
    if not 0<=r<=5:raise ValueError("Rating must be between 0 and 5.")
    b=Book(es["ISBN"].get().strip(),es["Title"].get().strip(),es["Author"].get().strip(),es["Category"].get().strip(),int(es["Year"].get()),r,n,n)
    self.lib.add_book(b);self.msg("Book added.");self.catalog()
   except Exception as e:self.msg(str(e),True)
  ttk.Button(f,text="Add Book",command=save).grid(row=7,column=1,sticky="w",padx=12,pady=10)
 def search(self):
  self.clear();self.head("Search Books","Search ISBN, title, author or category");bar=tk.Frame(self.body,bg=self.bg);bar.pack(anchor="w");q=ttk.Entry(bar,width=48);q.pack(side="left",padx=(0,8));t=self.table(("ISBN","Title","Author","Category","Year","Rating","Copies"))
  def run():
   if not q.get().strip():return self.msg("Enter a search term.",True)
   self.fill(t,self.lib.search(q.get()))
  ttk.Button(bar,text="Search",command=run).pack(side="left");q.bind("<Return>",lambda e:run())
 def manage(self):
  self.clear();self.head("Manage Books","Update or delete by ISBN");f=tk.Frame(self.body,bg="white",padx=20,pady=16);f.pack(anchor="nw",fill="x")
  labels=["ISBN","New Title","New Author","New Category","New Year","New Rating"];es={}
  for i,k in enumerate(labels):
   tk.Label(f,text=k,bg="white").grid(row=i,column=0,sticky="w",pady=5);es[k]=ttk.Entry(f,width=42);es[k].grid(row=i,column=1,padx=10,pady=5)
  def update():
   try:
    ch={}
    for k,v in [("New Title","title"),("New Author","author"),("New Category","category")]:
     if es[k].get().strip():ch[v]=es[k].get().strip()
    if es["New Year"].get().strip():ch["year"]=int(es["New Year"].get())
    if es["New Rating"].get().strip():ch["rating"]=float(es["New Rating"].get())
    self.lib.update_book(es["ISBN"].get().strip(),**ch);self.msg("Updated.");self.catalog()
   except Exception as e:self.msg(str(e),True)
  def delete():
   try:self.lib.delete_book(es["ISBN"].get().strip());self.msg("Deleted.");self.catalog()
   except Exception as e:self.msg(str(e),True)
  row=tk.Frame(f,bg="white");row.grid(row=6,column=1,sticky="w",pady=10);ttk.Button(row,text="Update",command=update).pack(side="left",padx=(0,8));ttk.Button(row,text="Delete",command=delete).pack(side="left")
 def recommend(self):
  self.clear();self.head("Recommendations","Graph BFS finds related books; max heap ranks them");bar=tk.Frame(self.body,bg=self.bg);bar.pack(anchor="w")
  tk.Label(bar,text="ISBN",bg=self.bg).pack(side="left");i=ttk.Entry(bar,width=28);i.pack(side="left",padx=8);n=ttk.Spinbox(bar,from_=1,to=20,width=5);n.set("5");n.pack(side="left")
  t=self.table(("ISBN","Title","Author","Category","Year","Rating","Copies"))
  def run():
   try:
    a=self.lib.recommend(i.get().strip(),int(n.get()));self.fill(t,a)
    if not a:self.msg("No recommendations. Check ISBN.",True)
   except Exception as e:self.msg(str(e),True)
  ttk.Button(bar,text="Recommend",command=run).pack(side="left",padx=8)
 def circulation(self):
  self.clear();self.head("Borrow / Return","Record circulation against a borrower");f=tk.Frame(self.body,bg="white",padx=22,pady=20);f.pack(anchor="nw",fill="x")
  tk.Label(f,text="ISBN",bg="white").grid(row=0,column=0,pady=7);i=ttk.Entry(f,width=40);i.grid(row=0,column=1,padx=10)
  tk.Label(f,text="Borrower",bg="white").grid(row=1,column=0,pady=7);b=ttk.Entry(f,width=40);b.grid(row=1,column=1,padx=10)
  def borrow():
   try:self.lib.borrow_book(i.get().strip(),b.get());self.msg("Borrowed.");self.dashboard()
   except Exception as e:self.msg(str(e),True)
  def ret():
   try:self.lib.return_book(i.get().strip(),b.get());self.msg("Returned.");self.dashboard()
   except Exception as e:self.msg(str(e),True)
  row=tk.Frame(f,bg="white");row.grid(row=2,column=1,pady=10,sticky="w");ttk.Button(row,text="Borrow",command=borrow).pack(side="left",padx=(0,8));ttk.Button(row,text="Return",command=ret).pack(side="left")
 def history(self):
  self.clear();self.head("Transaction History","Audit trail of library operations");t=self.table(("Action","ISBN","Title","Borrower","Timestamp"))
  for x in reversed(self.lib.transactions):t.insert("","end",values=(x.get("action"),x.get("isbn"),x.get("title"),x.get("borrower"),x.get("timestamp")))
 def analytics(self):
  self.clear();self.head("Performance Analysis","Benchmark custom search structures against linear search");area=tk.Frame(self.body,bg=self.bg);area.pack(fill="both",expand=True)
  def run():
   for w in area.winfo_children():w.destroy()
   r=run_benchmarks();fig,axs=plt.subplots(1,2,figsize=(10,4),dpi=90)
   axs[0].plot(r["size"],r["hash_ms"],marker="o",label="Hash");axs[0].plot(r["size"],r["linear_ms"],marker="o",label="Linear");axs[0].set_title("ISBN Search");axs[0].legend();axs[0].grid(alpha=.2)
   axs[1].plot(r["size"],r["avl_ms"],marker="o",label="AVL");axs[1].plot(r["size"],r["linear_title_ms"],marker="o",label="Linear");axs[1].set_title("Title Search");axs[1].legend();axs[1].grid(alpha=.2)
   fig.tight_layout();c=FigureCanvasTkAgg(fig,master=area);c.draw();c.get_tk_widget().pack(fill="both",expand=True);plt.close(fig)
  ttk.Button(self.body,text="Run Benchmarks",command=run).pack(anchor="w",pady=10)

if __name__=="__main__":
 root=tk.Tk();LibraryApp(root);root.mainloop()
