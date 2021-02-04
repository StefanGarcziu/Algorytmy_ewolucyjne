#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
Algorytm najbliższego sąsiada (zachłanny)
Algorytm zachłanny (greedy algorthm) optymalizuje efekt w najbliższym kroku, ale nie myśli o dalszej przyszłości!

Użytkownik sam podaje ilość miast - n, a także listę ich współrzędnych - cities .

'''

# biblioteka numeryczna
import numpy as np

# liczby losowe
import random

# grafika do wykresów
import matplotlib.pyplot as plt

# pomar czasu
import time

def greedy_algorthm(n, cities):
    #n=6 # użytkownik sam podaje ilość miejsc
    # cities=np.array([[random.random(),random.random()] for n in range(n)]) # Użytkownik sam podaje listę współrzędnych tych miast

    # odległość euklidesowa
    def dist(i,j):
        return np.sqrt((cities[i,0]-cities[j,0])**2 + (cities[i,1]-cities[j,1])**2)

    # długość drogi
    def len_path(path):
        return sum([dist(path[i],path[i+1]) for i in range(n)])

    def near_nei(ini):
        nn=[]
        to_visit=np.array([i for i in range(n)])
        ind=ini
        nn.append(ind)
        to_visit=np.delete(to_visit,ind)
        for k in range(n-1):
            ind0=np.argmin([dist(ind,i) for i in to_visit])
            ind=to_visit[ind0]
            nn.append(ind)
            to_visit=np.delete(to_visit,ind0)
        nn.append(ini)
        return nn

    to_visit=np.array([i for i in range(n)])

    ind=0

    to_visit=np.delete(to_visit,ind)

    ind0=np.argmin([dist(ind,i) for i in to_visit])

    nn=near_nei(1)

    tournn=np.array([cities[i] for i in nn]) # współrzędne trasy
    lnn=np.round(len_path(nn),3) # długość trasy

    plt.figure(figsize=(5,5))
    plt.title("Algorytm najbliższego sąsiada",fontsize=16) 
    plt.xlim(-.1,1.1)
    plt.ylim(-.1,1.1)

    plt.plot(tournn[:,0],tournn[:,1],c='blue')

    plt.scatter(cities[:,0],cities[:,1],c='red', s=30)

    plt.annotate(lnn, (.3,.95),fontsize=14)

    for i in range(n):
        plt.annotate(i, (cities[i,0], cities[i,1]),fontsize=14)

    plt.xlabel('$x$',fontsize=18)
    plt.ylabel('$y$',fontsize=18);

