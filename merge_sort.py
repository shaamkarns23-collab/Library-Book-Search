def merge_sort(items,key=lambda x:x):
    if len(items)<2: return list(items)
    m=len(items)//2; a=merge_sort(items[:m],key); b=merge_sort(items[m:],key)
    out=[]; i=j=0
    while i<len(a) and j<len(b):
        if key(a[i])<=key(b[j]): out.append(a[i]); i+=1
        else: out.append(b[j]); j+=1
    return out+a[i:]+b[j:]
