#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Brutalna siła (Brute force, BF) - sprawdzenie wszystkich możliwości
Inne nazwy: przegląd zupełny, metoda siłowa.

Użytkownik sam podaje ilość miast n, a także listę ich współrzędnych cities.

'''

# biblioteka numeryczna
import numpy as np

# liczby losowe
import random

# grafika do wykresów
import matplotlib.pyplot as plt

# pomar czasu
import time

from itertools import permutations # permutacje

def bf(n, cities):
    #n=10 # użytkownik sam podaje ilość miast
    #cities=np.array([[random.random(),random.random()] for n in range(n)]) # Użytkownik sam podaje listę współrzędnych tych miast

    # losowa droga - np.random.permutation 
    # dodanie miasta 0 na początku i na końcu
    sequence=np.insert(np.append(np.random.permutation(n-1)+1,0),0,0) # sekwencja miast z losową permutacją

    tour=np.array([cities[i] for i in sequence])

    # odległość euklidesowa
    def dist(i,j):
        return np.sqrt((cities[i,0]-cities[j,0])**2 + (cities[i,1]-cities[j,1])**2)

    # długość drogi
    def len_path(path):
        return sum([dist(path[i],path[i+1]) for i in range(n)])

    lenpa=np.round(len_path(sequence),3) # zaokrąglenie

    l=np.array([k for k in range(1,n)])
    all_perm=list(permutations(l))

    lp=len(all_perm) # liczba permutacji

    seq=[np.insert(np.append(all_perm[i],0),0,0) for i in range(lp)] 
    # dodanie miasta startowego na początku i na końcu
    
    # lista długości dla wszystkich tras
    all_len=[len_path(seq[i]) for i in range(lp)]

    # argument (pozycja elementu) listy długości dróg, który ma najmniejszą wartość
    imin=np.argmin(all_len)

    lopt=np.round(all_len[imin],3) # z zaokrągleniem

    # dodanie miasta startowego na początku i na końcu
    seqmin=np.insert(np.append(all_perm[imin],0),0,0)

    # współrzędne miast cyklu najlepszego rozwiązania
    tourmin=np.array([cities[i] for i in seqmin])
    
    plt_br=plt.figure(figsize=(5,5))
    plt.title("Najkrótsza droga",fontsize=16) 
    plt.xlim(-.1,1.1)
    plt.ylim(-.1,1.1)

    plt.plot(tourmin[:,0],tourmin[:,1],c='blue')

    plt.scatter(cities[:,0],cities[:,1],c='red', s=30)

    plt.annotate(lopt, (.8,.95),fontsize=14)

    plt.xlabel('$x$',fontsize=18)
    plt.ylabel('$y$',fontsize=18);

