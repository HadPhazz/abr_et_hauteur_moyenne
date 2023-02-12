from timeit import timeit
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from abr import Abr
import random
import math
import pandas as pd
import heapq

def randomTreeCreator(size):
    '''
    create a binary tree of a given size (nodes number) and return it
    '''
    abr = Abr()
    l = [k for k in range(size)]
    random.shuffle(l)
    for i in range(len(l)):
        abr = abr.insere(l[i])
    return abr

def average(liste):
    '''
    return the average value of the elements's sum in a list
    '''
    return sum(liste)/len(liste)

def averageTreeHeight(treeSize, n):
    '''
    return the average tree height based on the tree size and the nb of passes
    '''
    return average([randomTreeCreator(treeSize).hauteur() for i in range(n)])
    
def pointMoyen(Mi: list[tuple]) -> tuple[float]:
    """
    Renvoie les coordonnées du point moyen d'un nuage de points (sous la forme d'une liste triée de coordonnées (x, y)).
    """
    return (sum(M[0] for M in Mi)/len(Mi),
            sum(M[1] for M in Mi)/len(Mi))

def mayerAdjustment(x: list[float], y: list[float]) -> tuple[float]:
    """
    Renvoie les coefficients de la droite d'ajustement selon la méthode de Mayer
    """
    Mi = [(x[i], y[i]) for i in range(len(x))] #Création des couples de coordonnées
    Mi.sort()
    xa, ya = pointMoyen(Mi[:len(Mi)//2]) #Point moyen groupe des bottom 50 (50% des valeurs inférieures)
    xb, yb = pointMoyen(Mi[len(Mi)//2:]) #Point moyen groupe des top 50 (50% des valeurs supérieures)
    a = (yb - ya) / (xb - xa) # Coefficient a dans ax+b
    b = ya - a*xa # Reste b dans ax + b
    return (a, b)

def regressionLineaire(x: list[float], y: list[float]):
    """
    Renvoie les coefficients de la droite d'ajustement selon la méthode de la régression linéaire
    """
    varianceX = np.var(x)
    varianceY = np.var(y)
    covarianceXY = np.cov(x, y)[0][1]
    a = covarianceXY/varianceX
    b = average(y)-(a*(average(x)))
    r2 = a/varianceY #Coefficient r2, plus il est proche de 1, meilleur est la régression linéaire
    return (a, b, r2)

def plotter(treeSize, n):
    x = [i * 1 for i in range(1, treeSize+1)]
    y = [averageTreeHeight(i, n) for i in range(1, treeSize+1)]
    w = savgol_filter(y, treeSize, 2)
    plt.plot(x, w, 'o-', c="orange")
    plt.title("Hauteurs moyennes en fonction de la taille des arbres", fontsize=14)
    plt.xlabel("Taille de l'arbre", fontsize=12)
    plt.ylabel("Hauteur moyenne", fontsize=12)
    plt.grid()
    plt.show()

def scatter(treeSize, n):
    x = [math.log(i) for i in range(1, treeSize+1)]
    y = [averageTreeHeight(i, n) for i in range(1, treeSize+1)]
    Coords = [(x[i], y[i]) for i in range(len(x))] #Création des couples de coordonnées
    Coords.sort()
    xPointMoyen, yPointMoyen = pointMoyen(Coords) # x et y du point moyen du nuage
    yMayer = [mayerAdjustment(x, y)[0]*x[i]+(mayerAdjustment(x, y)[1]) for i in range(0, treeSize)] # ax+b with a and b using Mayer's adjustment
    yRegressionLineaire = [regressionLineaire(x, y)[0]*x[i]+(regressionLineaire(x, y)[1]) for i in range(0, treeSize)] #ax+b with a and b using linear regression's adjustment
    plt.plot(x, y, "o", c="orange", label="Hauteurs moyennes") # Plot des hauteurs moyennes, sous forme d'un nuage de point allongé
    plt.plot(x, yMayer, "-", c="blue", label="Droite d'ajustement de Mayer / a={:0.3f}, b={:0.3f}".format(mayerAdjustment(x, y)[0], mayerAdjustment(x, y)[1])) # Plot de la droite d'ajustement selon la méthode de Mayer
    plt.plot(x, yRegressionLineaire, "-", c="green", label="Droite d'ajustement par regression linéaire / a={:0.3f}, b={:0.3f}".format(regressionLineaire(x, y)[0], regressionLineaire(x, y)[1])) # Plot de la droite d'ajustement selon la méthode de régression linéaire
    plt.plot(xPointMoyen, yPointMoyen, "o", c="red", label="Point moyen / {:0.3f}".format(average(y))) # Plot du point moyen du nuage de point (qui correspond à la hauteur moyenne des arbres)
    plt.title("Hauteurs moyennes et droites d'ajustement", fontsize=14)
    plt.xlabel("log(taille_arbre)", fontsize=12)
    plt.ylabel("Hauteur moyenne", fontsize=12)
    plt.grid()
    plt.legend()
    plt.show()
    
######################################TESTS##############################################################
    
def nMaxValues(liste):
    lst = pd.Series(liste)
    maxValues = lst.nlargest(len(liste)//10).values.tolist()
    return maxValues

def nMinValues(liste):
    lst = pd.Series(liste)
    minValues = lst.nsmallest(len(liste)//10).values.tolist()
    return minValues
    
def main(treeSize, n):
    listLog = [math.log(i) for i in range(1, treeSize+1)] # Liste des log(n) où n = treeSize
    y = [averageTreeHeight(i, n) for i in range(1, treeSize+1)]
    aMayer = mayerAdjustment(listLog, y)[0]
    bMayer = mayerAdjustment(listLog, y)[1]
    aLR = regressionLineaire(listLog, y)[0]
    bLR = regressionLineaire(listLog, y)[1]
    deltaListMayer = []
    deltaListLR = []
    print("Size	|Average Height	|Average Height w/ Mayer's ax+b	|Average Height w/ Linear Regression's ax+b	|Difference w/ Mayer	|Difference w/ LR")
    for i in range(1, treeSize+1):
        deltaMayer = y[i-1]-(aMayer*listLog[i-1]+bMayer) # Différence entre la hauteur moyenne d'un arbre PAR LES TESTS et PAR LE CALCUL DE MAYER
        deltaLR = y[i-1]-(aLR*listLog[i-1]+bLR) # Différence entre la hauteur moyenne d'un arbre PAR LES TESTS et PAR LE CALCUL DE MAYER
        deltaListMayer.append(deltaMayer)
        deltaListLR.append(deltaLR)
        print("{}	|{:0.3f}		|{:0.3f}				|{:0.3f}						|{:0.3f}			|{:0.3f}			".format(i, y[i-1],(aMayer*listLog[i-1]+bMayer), (aLR*listLog[i-1]+bLR), deltaMayer, deltaLR))
    highestDeltaMayer = []
    lowestDeltaMayer = []
    highestDeltaLR = []
    lowestDeltaLR = []
    for i in range(len(deltaListLR)):
        highMayer = max(0-deltaListMayer[i],deltaListMayer[i]-0)
        highestDeltaMayer.append(highMayer)
        lowMayer = min(0-deltaListMayer[i],deltaListMayer[i]-0)
        lowestDeltaMayer.append(lowMayer)
        highLR = max(0-deltaListLR[i],deltaListLR[i]-0)
        highestDeltaLR.append(highLR)
        lowLR = min(0-deltaListLR[i],deltaListLR[i]-0)
        lowestDeltaLR.append(lowLR)
    print("Mayer's a : {:0.3f}, Mayer's b : {:0.3f}".format(aMayer, bMayer))
    print("LR's a : {:0.3f}, LR's b : {:0.3f}".format(aLR, bLR))
    print("Highest Δ Mayer : {:0.3f} | Lowest Δ Mayer : {:0.3f}".format(max(highestDeltaMayer), max(lowestDeltaMayer)))
    print("Highest Δ LR : {:0.3f} | Lowest Δ LR : {:0.3f}".format(max(highestDeltaLR), max(lowestDeltaLR)))
