#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
# grafika do wykresów
import matplotlib.pyplot as plt
# pomar czasu
import time
# wyświetlanie importowanej grafiki
from IPython.display import display, Image



def opt2(n, cities):
    def opt2(route,i,j): # zakładamy, że zakresy wskaźników sprawdzamy przed użyciem
        return np.concatenate((route[:i],np.flip(route[i:(j+1)]),route[(j+1):]))
    
    def ranopt2(route): # 2-opt w losowym miejscu
        n=len(route)-1
        i=np.random.randint(1,n-2)
        j=np.random.randint(i+1,n-1)    
        return opt2(route,i,j)
    
    # odległość euklidesowa
    def dist(i,j):
            return np.sqrt((cities[i,0]-cities[j,0])**2 + (cities[i,1]-cities[j,1])**2)
    # tablica odległości
    dtab=np.array([[dist(i,j) for i in range(n)] for j in range(n)])
    
    # długość drogi
    def len_path(path):
    #    for i in range(n): # test, czy zakresy OK
    #        print(i,i+1,path[i],path[i+1])
        return sum([dtab[path[i],path[i+1]] for i in range(n)])    
    
    
    seq=np.insert(np.append(np.random.permutation(n-1)+1,0),0,0) 
                                    # losowa sekwencja miast
    lenseq=len_path(seq) # początkowa długość   
    num_steps=2000 # liczba kroków (losowań)

    for i in range(num_steps):
        newseq=ranopt2(seq) # nowa trasa
        lennewseq=len_path(newseq) # można szybciej dla symetrycznego
        if lennewseq<lenseq: # jeśli nowa trasa jest krótsza
            seq=newseq
            lenseq=lennewseq
            
    
    def rep(f, n):
        if n == 1:
            return f
        else:
            return lambda x: f(rep(f,n-1)(x)) # rekurencja    
    
    def test_f(x):
        return np.sqrt(x)
    
    def ran_2opt_n(d_tab,n_steps,n_rep):
        n=len(dtab)
        seq=np.insert(np.append(np.random.permutation(n-1)+1,0),0,0) 
                                    # losowa sekwencja miast
        lenseq=len_path(seq)    
    
        for i in range(n_steps):
            newseq=rep(ranopt2,n_rep)(seq) # n_rep kroków 2-opt
            lennewseq=len_path(newseq)
            if lennewseq<lenseq:
                seq=newseq
                lenseq=lennewseq                
        return(seq)
    
    tour=np.array([cities[i] for i in seq])

    plt.figure(figsize=(5,5))
    plt.title("2-opt x n losowo",fontsize=16) 
    plt.xlim(-.1,1.1)
    plt.ylim(-.1,1.1)

    plt.scatter(cities[:,0],cities[:,1],c='red', s=20)
    plt.plot(tour[:,0],tour[:,1],c='blue')
    plt.annotate(np.round(len_path(seq),4), (.8,.95),fontsize=14);

