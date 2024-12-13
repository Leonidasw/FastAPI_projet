import tkinter as tk
from random import randint
from enum import Enum

def init_plateau(taille:int, val:int)->list:
    """
    Hyp: Une fonction qui prend une taille et une valeur et retourne un plateau carré dont toutes les cases sont
initialisées avec la valeur passée en paramètre.
    """
    return [[val for i in range(taille)] for i in range(taille)]

def init_mine(plateau:list, nb_mines:int, case_U:list)->list:
    """
    Hyp: une fonction qui prend en paramètre un plateau et le nombre de mines `a placer et retourne l’ensemble des
coordonnées des mines.
    """
    taille = len(plateau)
    liste_mines = []
    while len(liste_mines) < nb_mines:
        y, x = randint(0, taille-1), randint(0, taille-1)
        if (x, y) not in liste_mines and (x, y) not in case_U:
            liste_mines.append((x, y))
    return liste_mines

def liste_voisins(coord:tuple, taille:int)->list:
    """
    Hyp: une fonction qui prend les coordonnées d’une case et la taille du plateau et retourne la liste des coor-
données des cases voisines.
    """
    x_coord,y_coord=coord[0],coord[1]
    liste = []
    liste_def = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x != 0 or y != 0:
                liste.append((x_coord+x, y_coord+y))
    for element in liste:
        if element[0] >= 0 and element[1] >= 0 and element[0] < taille and element[1] < taille:
            liste_def.append(element)
    return liste_def

def init_compte(plateau:list, liste_mines:list)->list:
    """
    Hyp: une fonction qui prend en paramètre un plateau et un ensemble de coordonnée et qui pour toutes les cases
voisines aux mines compte le nombre de mines adjacentes.  
    """
    taille = len(plateau)
    for mine in liste_mines:
        voisins = liste_voisins(mine, taille)
        for voisin in voisins:
            x_voisin, y_voisin = voisin
            if plateau[x_voisin][y_voisin] != 9:
                plateau[x_voisin][y_voisin] += 1
    return plateau

def init_plateau_mine(taille:int, nb_mines:int, case_U:list)->list:
    """
    Hyp: une fonction qui prend en param`etre une taille et un nombre de mines et initialise le plateau des
mines avec le nombre de mines adjacentes dans les cases sans mines.
    """
    plateau = init_plateau(taille, 0)
    liste_mines = init_mine(plateau, nb_mines, case_U)
    for mine in liste_mines:
        x_mine,y_mine=mine[0],mine[1]
        plateau[x_mine][y_mine] = 9
    plateau = init_compte(plateau, liste_mines)
    return plateau
    


