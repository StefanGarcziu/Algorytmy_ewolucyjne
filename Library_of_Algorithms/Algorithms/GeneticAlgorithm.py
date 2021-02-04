#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Algorytm Genetyczny -  Genetic Algorithm, GA.

GA jest jedną z ewolucyjnych metod optymalizacji. Zalicza się go do klasy algorytmów heurystycznych. 
Przeszukiwanie możliwych rozwiązań w celu znalezienia rozwiązania najlepszego lub potencjalnie 
najlepszego odbywa się za pomocą mechanizmów ewolucji oraz doboru naturalnego.

"""

import numpy as np

# liczby losowe
import random

# grafika do wykresów
import matplotlib.pyplot as plt
import matplotlib as mpl

# działania na łańcuchach znaków
import string 

# statystyka
import statistics as st

# pomar czasu
import time

def GA(n, npop, start, cities):
    
    # odleglość euklidesowa między miastami pośrednimi i oraz j
    def dist(i,j):
        return np.sqrt((cities[i,0]-cities[j,0])**2 + (cities[i,1]-cities[j,1])**2)

    # odległość miasta i od miasta startowego
    def dist_s(i):
        return np.sqrt((cities[i,0]-start[0])**2 + (cities[i,1]-start[1])**2)
    
    # tablice odległości między miastami
    dtab=np.array([[dist(i,j) for i in range(n-1)] for j in range(n-1)]) # ...pośrednimi
    dtab_s=np.array([dist_s(i) for i in range(n-1)]) # ...od miasta startowego
    
    def len_path(path):
        return dtab_s[path[0]]+sum(dtab[path[i],path[i+1]] 
                               for i in range(n-2))+dtab_s[path[n-2]]
    
    # chromosom/osobnik jako losowa permutacja (ciag miast pośrednich)
    def person():
        return np.random.permutation(n-1)  
    
    # początkowe (losowe) pokolenie - tablica osobników
    popul=np.array([person() for _ in range(npop)])
    
    # długości dróg dla początkowego pokolenia
    popul_len=np.array([len_path(pers) for pers in popul])
    
    # tablica w formacie [droga, jej długosć]
    comb=np.array([[popul[i], popul_len[i]] for i in range(npop)],dtype=object)
    
    popul_c=np.array(sorted(comb, key=lambda x: x[1]))
    
    # selekcja liczby n_best najlepszych osobników z populacji popu

    def select(popu,n_best):
    
        le=len(popu) # liczebność populacji
        popu_len=np.array([len_path(pers) for pers in popu]) # długości dróg 
    
        # sortowanie
        com=np.array([[popu[i], popu_len[i]] for i in range(len(popu_len))],dtype=object)
                                   # tablica z dołączonymi długościami dróg
        popu_c=sorted(com, key=lambda x: x[1]) # sortowanie wg długości drogi
        p_c=[x[0] for x in popu_c] # posortowana tablica dróg bez długości
    
        sel=np.array([p_c[0]])     # dodanie najkrótszej drogi do nowej populacji sel
        k=1 # aktualna liczba dróg w populacji sel
    
        for i in range(1,le): # osobnik [0] już dodany, zaczynamy od [1]
        
            if not np.array_equal(p_c[i],sel[-1]): # dodaj tylko innego osobnika
                k=k+1 # aktualna liczba dróg w populacji sel
                sel=np.append(sel,p_c[i]) # dodanie osiobnika do nowej populacji sel
            
            sel=np.reshape(sel,[k,n-1]) # przeformatowanie tablicy zob. poniżej
            if k==n_best: # skończ, jeśli masz już n_best osobników
                break
        return sel    # nowa populacja
    
    i1=random.randint(0,npop-1)
    i2=random.randint(0,npop-1)
    
    # mutacja: zamiana miejscami dwóch genów
    def swap(list, p1, p2): 
        list[p1], list[p2] = list[p2], list[p1] 
        return list
    
    nummut=n//20 # liczba prób mutacji
    mut=0.3 # prawdopodobieństwo mutacji w jednej próbie
    
    # jak wyżej, ale bez pisania testowego, ale z dodaniem mutacji

    def breed(papa, mama):
        cut=random.randint(1,n-2)   
        chp=np.delete(papa, np.arange(cut, n-1, 1))
        chm=np.delete(mama, np.arange(0,cut, 1))
        if random.random() > 0.5:
            chm=np.flip(chm)
        child=np.concatenate((chp,chm),axis=0)
        repeated=np.intersect1d(chp,chm)
        missed=np.setdiff1d(papa, child)
        random.shuffle(missed)
        for i in range(len(repeated)):
            icor=np.where(child==repeated[i])[0]
            child[random.choice(icor)]=missed[i]
        
        for _ in range(nummut): # mutacje, powtórz nummut razy
            if random.random()<mut: # przestaw z prawdopodobieństwem mut parę losowych miast
                swap(child, random.randint(0,n-2),random.randint(0,n-2))
        return child
    
    # wekreowanie nowego pokolenia
    def generation():

        children=np.array([breed(popul[random.randint(0,npop-1)],                                 popul[random.randint(0,npop-1)]) for _ in range(nchil)]) 
                                  # spłodzenie dzieci
    
        al=np.concatenate((popul,children)) # dodanie dzieci do populacji rodziców
    
        return select(al,npop)  # selekcja npop najlepszych osobników z połączonej populacji
    
    # parametry
    npop=3*n
    nchil=3*npop
    mut=.7
    nummut=n//15

    # inicjalizacja
    popul=np.array([person() for _ in range(npop)])
    per=np.array(len_path(popul[0]))
    
    for i in range(50):    
        for _ in range(50):
            popul=generation()
        per=np.append(per,len_path(popul[0])) 
        
    tmin=popul[0]
    # print(tmin)

    tourmin=np.array([cities[i] for i in tmin])
    tourmin=np.reshape(np.append(np.insert(tourmin,0,start),start),[n+1,2])
    # print(tourmin)

    plo_GA=plt.figure(figsize=(5,5))
    plt.title("GA",fontsize=16) 
    plt.xlim(-.1,1.1)
    plt.ylim(-.1,1.1)

    plt.plot(tourmin[:,0],tourmin[:,1],c='blue')

    plt.scatter(cities[:,0],cities[:,1],c='blue', s=30)
    plt.scatter(start[0],start[1],c='red', s=30)

    lenpa=np.round(len_path(tmin),3)

    plt.annotate(lenpa, (.87,1.03),fontsize=14)

    plt.xlabel('$x$',fontsize=18)
    plt.ylabel('$y$',fontsize=18);    

