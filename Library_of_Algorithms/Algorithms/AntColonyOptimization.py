#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Algorytm mrówkowy - Ant Colony Optimization, ACO. 

Mrówka, niosąc pokarm z F do mrowiska (gniazda) N, zostawia na ścieżce feromon. 
Kolejne mrówki wybierają preferencyjnie tę drogę, gdzie jest najwięcej feromonu. 
Po pewnym czasie zostaje znaleziona optymalna trasa!

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

# skumulowana suma tablicy
from itertools import accumulate

def aco(n, cities):
    # n=10 # użytkownik sam podaje ilość miast
    # cities=np.array([[random.random(),random.random()] for n in range(n)]) # Użytkownik sam podaje listę współrzędnych tych miast

    # odległość euklidesowa
    def dist(i,j):
        return np.sqrt((cities[i,0]-cities[j,0])**2 + (cities[i,1]-cities[j,1])**2)

    # długość drogi
    def len_path(path):
        return sum([dist(path[i],path[i+1]) for i in range(n)])

    # zebranie powyższych instrukcji w jedną funkcję
    def ind_prob(tab_p):
        cum_p=np.array(list(accumulate(tab_p)))
        return np.sum(np.heaviside(random.random()-cum_p,0)).astype(int)

    # Zwraca (losowo) miasto do odwiedzenia z listy miast togo, jeśli mrówka jest w mieście i.
    # Stosujemu oczywiście naszą maszynke ind_prob.
    def ac_next(i, togo):
        p =np.array([fero[i, j]**alpha/dis_tab[i, j]**beta for j in togo]) # wagi
        su=np.sum(p) # suma wag
        p=p/su # prawdopodobieństwa (wagi znormalizowane do 1)
        return togo[ind_prob(p)]

    # tablica odległości między miastami
    dis_tab=np.array([[dist(i,j) for i in range(n)] for j in range(n)])

    fero=np.array([[1. for _ in range(n)] for _ in range(n)])-np.identity(n)

    # tablica prawdopodobieństw
    tab_p=np.array([0.5, 0.2, 0.1, 0.2])
    cum_p=np.array(list(accumulate(tab_p)))

    # parametry modelu dot. prawdopodobieństwa wyboru drogi przez mrówkę
    alpha = 1.15;
    beta = 1;

    h = 0.03; # szybkość uaktualniania śladów feromonowych
    # po kolejnym etapie algorytmu feromony_nowe = (1-h) feromony_stare + h feromony_złożone

    popsize = 10; # liczba mrówek "na trasie" w kolejnym etapie algorytmu

    sc = n/popsize; # kontroluje, ile feromonu jest zostawiane = liczba miast/liczba mrówek
    # odkładana przez mrówkę ilość feromonu to sc/długość odcinka

    to_v=[i for i in range(1,n)] # miasta do odwiedzenia (na razie wszystkie)

    tt=[ac_next(0,to_v) for _ in range(10000)] # 10000 wyborów (na próbę)

    pop = 15  
    
    pos=random.randint(0,n-1)

    route=[pos]

    # miasta do odwiedzenia
    to_v=[i for i in range(0,pos)]+[i for i in range(pos+1,n)]

    # jeden etap algorytmu
    # liczba pop mrówek wyrusza w trasę, każda z losowo wybranego miasta
    
    def ac_one(pop): 
        lm=10**10
        global fero2
        fero2=np.array([[0. for _ in range(n)] for _ in range(n)])
        for _ in range(pop):
            pos=random.randint(0,n-1)
            route=[pos]
            to_v=[i for i in range(0,pos)]+[i for i in range(pos+1,n)]
        
            for _ in range(n-1):
                pos=ac_next(pos,to_v)
                route.append(pos)
                to_v.remove(pos)
            
            route.append(route[0])        
        
            lr=len_path(route)

            if lr<lm:
                lm=lr
                r_opt=route
             
        for i in range(n):
            fero2[r_opt[i],r_opt[i+1]]=fero2[r_opt[i],r_opt[i+1]]+sc/lm
            fero2[r_opt[i+1],r_opt[i]]=fero2[r_opt[i+1],r_opt[i]]+sc/lm
        
          
        return lm, r_opt

    # cały algorytm mrówkowy dla TSP (10 linijek + 20 linijek kodu ac_one)

    iter=10000 # liczba iteracji

    min_l=10**10 # coś dużego, początkowa długość najlepszej drogi (numeryczna nieskonczoność)
    fero=np.array([[1. for _ in range(n)] for _ in range(n)])-np.identity(n) 
         # początkowa macierz feromonów

    for k in range(iter):   # pętla po iteacjach
        opt=ac_one(popsize) # jeden "zespół" popsize mrówek na trasie

        if opt[0]<min_l: # jeśli znaleziona droga krótsza, uaktualnij ...
            min_l=opt[0] # ... jej długość ...
            best_route=opt[1] # ... i trasę
    # ważne!         
        fero=(1-h)*fero+h*fero2 # uaktualnienie macierzy feromonów
            # parowanie "starego" feromonu, dodanie nowego

    print(round(min_l,3), best_route) # najlepsza trasa    

    plt.figure(figsize=(5,5))
    plt.title("Mrówki",fontsize=16) 
    plt.xlim(-.1,1.1)
    plt.ylim(-.1,1.1)

    # grafika ilustrujaca gęstość feromonów poprzez grubość linii
    for i in range(n):
        for j in range(n):
            plt.plot([cities[i,0],cities[j,0]],[cities[i,1],cities[j,1]],
            c="gray",linewidth=3*fero[i,j]) # grubosć linii prop. do gestości feromonów

    bb=np.array([cities[i] for i in best_route])
    plt.plot(bb[:,0],bb[:,1],c='blue',linewidth=2)

    mm=np.round(min_l,3)
    plt.annotate(mm, (.3,1),fontsize=14)
    #for i in range(n):
        #plt.annotate(i, (cities[i,0], cities[i,1]),fontsize=14)

    plt.xlabel('$x$',fontsize=18)
    plt.ylabel('$y$',fontsize=18);

