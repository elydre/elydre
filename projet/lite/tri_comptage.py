import random
from time import time
from sys import setrecursionlimit

MAX = 1000

def tri_cool(l):
    refs = [0 for i in range(MAX)]
    for i in l:
        refs[i] += 1
    ret = []
    for i in range(MAX):
        if refs[i] > 0:
            ret.append(i)
    return ret

def tri_fusion(l):
    if len(l) <= 1:
        return l
    m = len(l) // 2
    l1 = tri_fusion(l[:m])
    l2 = tri_fusion(l[m:])
    ret = []
    i = j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            ret.append(l1[i])
            i += 1
        else:
            ret.append(l2[j])
            j += 1
    while i < len(l1):
        ret.append(l1[i])
        i += 1
    while j < len(l2):
        ret.append(l2[j])
        j += 1
    return ret

setrecursionlimit(1000000)

def tri_zoli(l):
    if len(l) <= 1:
        return l
    pivot = l[0]
    l1 = [i for i in l[1:] if i < pivot]
    l2 = [i for i in l[1:] if i >= pivot]
    return tri_zoli(l1) + [pivot] + tri_zoli(l2)

def gen_list(n):
    return [random.randint(0, MAX - 1) for _ in range(n)]

def timeit(func, l):
    d = time()
    func(l)
    return (time() - d) * 1000

if __name__ == "__main__":
    l = gen_list(100)
    print("list generated!")

    print("Tri cool: ", timeit(tri_cool, l))
    print("Tri fusion: ", timeit(tri_fusion, l))
    print("Tri zoli: ", timeit(tri_zoli, l))
