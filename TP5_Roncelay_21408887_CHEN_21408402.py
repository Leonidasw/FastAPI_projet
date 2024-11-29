import tkinter as tk
from random import randint
from enum import Enum

def init_plateau(taille:int, val:int)->list:
    """
    Hyp: Une fonction qui prend une taille et une valeur et retourne un tableau carré dont toutes les cases sont
initialisées avec la valeur passée en paramètre.
    """
    return [[val for i in range(taille)] for i in range(taille)]

def init_mine(tableau:list, nb_mines:int)->list:
    """
    Hyp: une fonction qui prend en paramètre un tableau et le nombre de mines `a placer et retourne l’ensemble des
coordonnées des mines.
    """
    taille = len(tableau)
    liste_mines = []
    while len(liste_mines) < nb_mines:
        x, y = randint(0, taille-1), randint(0, taille-1)
        if (x, y) not in liste_mines:
            liste_mines.append((x, y))
    return liste_mines

def liste_voisins(coord:tuple, taille:int)->list:
    """
    Hyp: une fonction qui prend les coordonnées d’une case et la taille du tableau et retourne la liste des coor-
données des cases voisines.
    """
    liste = []
    liste_def = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x != 0 or y != 0:
                liste.append((coord[1]+y, coord[0]+x))
    for element in liste:
        if element[0] >= 0 and element[1] >= 0 and element[0] < taille and element[1] < taille:
            liste_def.append(element)
    return liste_def

def init_compte(tableau:list, liste_mines:list)->list:
    """
    Hyp: une fonction qui prend en paramètre un tableau et un ensemble de coordonnée et qui pour toutes les cases
voisines aux mines compte le nombre de mines adjacentes.  
    """
    taille = len(tableau)
    for mine in liste_mines:
        x_mine, y_mine = mine
        voisins = liste_voisins(mine, taille)
        for voisin in voisins:
            x_voisin, y_voisin = voisin
            if tableau[x_voisin][y_voisin] != 9:
                tableau[x_voisin][y_voisin] += 1
    return tableau

def init_plateau_mine(taille:int, nb_mines:int)->list:
    """
    Hyp: une fonction qui prend en param`etre une taille et un nombre de mines et initialise le plateau des
mines avec le nombre de mines adjacentes dans les cases sans mines.
    """
    tableau = init_plateau(taille, 0)
    liste_mines = init_mine(tableau, nb_mines)
    for element in liste_mines:
        tableau[element[1]][element[0]] = 9
    tableau = init_compte(tableau, liste_mines)
    return tableau

nb_mines = 30
taille = 10
#tableau_jeu = init_plateau_mine(taille, nb_mines)
tableau_jeu=[[0, 1, 9, 2, 2, 1, 3, 9, 9, 9], [2, 3, 4, 9, 3, 9, 3, 9, 4, 2], [9, 9, 3, 9, 3, 2, 4, 4, 3, 1], [9, 3, 3, 2, 2, 1, 9, 9, 9, 2], [1, 1, 1, 9, 2, 3, 4, 9, 4, 9], [0, 0, 2, 3, 9, 4, 9, 3, 2, 1], [1, 1, 2, 9, 5, 9, 9, 2, 0, 0], [1, 9, 3, 4, 9, 9, 3, 2, 1, 1], [1, 2, 9, 4, 9, 3, 1, 1, 9, 2], [0, 1, 2, 9, 2, 1, 0, 1, 2, 9]]

def afficher_plateau_tkinter(plateau:list):
    """
    Hyp: Une fonction d'affichage pour vérifier nos fonctions.
    
    """
    root = tk.Tk()
    root.title("Affichage du plateau de mines")
    
    taille = len(plateau)
    
    for i in range(taille):
        for j in range(taille):
            val = plateau[i][j]
            
            if val == 9:  # Mine
                color = "red"
            elif val == 0:
                color = "white"
            elif val == 1:
                color = "lightblue"
            elif val == 2:
                color = "blue"
            elif val == 3:
                color = "green"
            elif val == 4:
                color = "yellow"
            elif val == 5:
                color = "orange"
            elif val >= 6:
                color = "purple"
            
            label = tk.Label(root, text=str(val), width=4, height=2, bg=color, relief="solid", borderwidth=1)
            label.grid(row=i, column=j)
    
    root.mainloop()

#afficher_plateau_tkinter(tableau_jeu)

class Status(Enum):
    COVERED = nb_mines = 30
    taille = 10
    #tableau_jeu = init_plateau_mine(taille, nb_mines)
    UNCOVERED = 2
    MARK = 3

def afficher_plateau_statut(plateau_statut:list):
    """
    Hyp: Une fonction d’affichage, qui affiche le plateau de jeu selon le statut de chaque case
    """
    for ligne in plateau_statut:
        for case in ligne:
            if case == Status.COVERED:
                print('C', end=' ')  
            elif case == Status.UNCOVERED:
                print('U', end=' ')  
            elif case == Status.MARK:
                print('M', end=' ')  
        print() #Retour à la ligne


def init_statut_plateau(taille:int)->list:
    """
    Hyp: Initialise le tableau de statut pour voir tout le plateau
    """
    return [[Status.COVERED for _ in range(taille)] for _ in range(taille)]


# Exemple d'utilisation
plateau_statut = init_statut_plateau(taille)
#afficher_plateau_statut(plateau_statut)

def decouvre_case(coord:tuple,tableau_jeu:list,tableau_statut:list)->bool:
    """
    Hyp: une fonction qui prend en paramètre les coordonnées d’une case, le plateau de jeu et le plateau de statut, d´ecouvre la case et
retourne vrai si la case d´ecouverte n’est pas une mine
    """    
    tableau_statut[coord[1]][coord[0]]=Status.UNCOVERED
    if tableau_jeu[coord[1]][coord[0]]!=9:
        return True
    return False

def mark_stat(coord:tuple,tableau_jeu:list,tableau_statut:list):
    """
    Hyp: une fonction qui prend en paramètre les coordonn´ees d’une case, le plateau de jeu et le plateau de statut, marque la case si
celle-ci est couverte et non-marqu´e ou enl`eve la marque si celle-ci était déjà marquée.
    """    
    if tableau_statut[coord[1]][coord[0]]==Status.MARK:
        tableau_statut[coord[1]][coord[0]]=Status.COVERED
    else: 
        tableau_statut[coord[1]][coord[0]]=Status.MARK
        
def nb_voisin_MARK(coord:tuple,tableau_statut:list)->int:
    """
    Hyp: Compte le nombre de case marqué autour d'une coord
    """    
    nb=0
    taille=len(tableau_statut)
    voisins = liste_voisins(coord, taille)
    for voisin in voisins:
        x_voisin, y_voisin = voisin
        if tableau_statut[x_voisin][y_voisin]==Status.MARK:
            nb+=1
    return nb
        
def decouvre_voisin(coord:tuple,tableau_jeu:list,tableau_statut:list)->bool:
    """
    Hyp:  une fonction qui prend en param`ère les coordonnées d’une case, le plateau de jeu et le plateau de statut. Elle d´ecouvre toutes
les cases voisines si le nombre de cases marqu´ees est ´egale au nombre de mines voisines. La fonction retourne vrai si il n’y aucune
mine sur les cases d´ecouvertes.   
    """
    taille=len(tableau_statut)
    nb_voisin_marquer=nb_voisin_MARK(coord, tableau_statut)
    if tableau_statut[coord[1]][coord[0]]==Status.UNCOVERED and tableau_jeu[coord[1]][coord[0]]==nb_voisin_marquer:
        voisins = liste_voisins(coord, taille)
        for voisin in voisins:
            x_voisin, y_voisin = voisin
            if tableau_statut[x_voisin][y_voisin]!=Status.MARK:
                if tableau_jeu[x_voisin][y_voisin]==9:
                    return False
                tableau_statut[x_voisin][y_voisin]=Status.UNCOVERED
        return True
        

plateau_statut[0][2]=Status.MARK
plateau_statut[1][3]=Status.MARK
plateau_statut[2][3]=Status.MARK
plateau_statut[2][1]=Status.MARK
plateau_statut[1][2]=Status.UNCOVERED


def afficher_plateau(tableau_jeu:list,tableau_statut:list):
    for ligne in range(len(plateau_statut)):
        for case in range(len(plateau_statut[ligne])):
            if tableau_statut[ligne][case] == Status.COVERED:
                print('C', end=' ')  
            elif tableau_statut[ligne][case] == Status.UNCOVERED:
                print(tableau_jeu[ligne][case],end=' ')  
            elif tableau_statut[ligne][case] == Status.MARK:
                print('M', end=' ')  
        print() #Retour à la ligne



"""
    
    Démarrer le jeu

"""

nb_mines = 20
taille = 10
tableau_jeu = init_plateau_mine(taille, nb_mines)
afficher_plateau_tkinter(tableau_jeu)
plateau_statut = init_statut_plateau(taille)
afficher_plateau_statut(plateau_statut)

def action(mot:str)->tuple:
    mettre_int=mot[1:].split(',')
    chiffre_liste=[]
    for chiffre in mettre_int:
        chiffre_liste.append(int(chiffre))
    coord=tuple(chiffre_liste)
    return ('mark',coord) if mot[0]=='m' else ('uncover',coord)

game=True
while game==True:
    action_joueur=action(input("Met les cordonnées de la case tu veux marqué ou déminé (par ex: m1,2, u1,2) : "))
    if action_joueur[0]=='mark':
        mark_stat(action_joueur[1], tableau_jeu, plateau_statut)
        afficher_plateau(tableau_jeu, plateau_statut)
    else:
        if decouvre_case(action_joueur[1], tableau_jeu,plateau_statut)==False:
            print("Tu as perdu!")
            game=False
        decouvre_voisin(action_joueur[1], tableau_jeu, plateau_statut)
        afficher_plateau(tableau_jeu , plateau_statut)     
    nb_mark=0
    nb_covered=0
    for ligne in range(len(plateau_statut)):
        for case in range(len(plateau_statut[ligne])):
            if plateau_statut[ligne][case] == Status.COVERED:
                nb_covered+=1
            if plateau_statut[ligne][case] == Status.MARK:
                nb_mark+=1
    if nb_mark==nb_mines and 0==nb_covered:
        print("Tu as gagnée")
        game=False



