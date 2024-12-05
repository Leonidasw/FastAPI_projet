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
        x_mine, y_mine = mine
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

class Status(Enum):
    COVERED = 1
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
    Hyp: Initialise le plateau de statut pour voir tout le plateau
    """
    return [[Status.COVERED for _ in range(taille)] for _ in range(taille)]

def decouvre_case(coord:tuple,plateau_jeu:list,plateau_statut:list)->bool:
    """
    Hyp: une fonction qui prend en paramètre les coordonnées d’une case, le plateau de jeu et le plateau de statut, d´ecouvre la case et
retourne vrai si la case d´ecouverte n’est pas une mine
    """    
    plateau_statut[coord[0]][coord[1]]=Status.UNCOVERED
    if plateau_jeu[coord[0]][coord[1]]!=9:
        return True
    return False

def mark_stat(coord:tuple,plateau_jeu:list,plateau_statut:list):
    """
    Hyp: une fonction qui prend en paramètre les coordonn´ees d’une case, le plateau de jeu et le plateau de statut, marque la case si
celle-ci est couverte et non-marqu´e ou enl`eve la marque si celle-ci était déjà marquée.
    """    
    if plateau_statut[coord[0]][coord[1]]==Status.MARK:
        plateau_statut[coord[0]][coord[1]]=Status.COVERED
    else: 
        plateau_statut[coord[0]][coord[1]]=Status.MARK
        
def nb_voisin_MARK(coord:tuple,plateau_statut:list)->int:
    """
    Hyp: Compte le nombre de case marqué autour d'une coord
    """    
    nb=0
    taille=len(plateau_statut)
    voisins = liste_voisins(coord, taille)
    for voisin in voisins:
        x_voisin, y_voisin = voisin
        if plateau_statut[x_voisin][y_voisin]==Status.MARK:
            nb+=1
    return nb
        
def decouvre_voisin(coord:tuple,plateau_jeu:list,plateau_statut:list)->bool:
    """
    Hyp:  une fonction qui prend en param`ère les coordonnées d’une case, le plateau de jeu et le plateau de statut. Elle d´ecouvre toutes
les cases voisines si le nombre de cases marqu´ees est ´egale au nombre de mines voisines. La fonction retourne vrai si il n’y aucune
mine sur les cases d´ecouvertes.   
    """
    taille=len(plateau_statut)
    nb_voisin_marquer=nb_voisin_MARK(coord, plateau_statut)
    if plateau_statut[coord[0]][coord[1]]==Status.UNCOVERED and plateau_jeu[coord[0]][coord[1]]==nb_voisin_marquer:
        voisins = liste_voisins(coord, taille)
        for voisin in voisins:
            x_voisin, y_voisin = voisin
            if plateau_statut[x_voisin][y_voisin]!=Status.MARK:
                if plateau_jeu[x_voisin][y_voisin]==9:
                    return False
                plateau_statut[x_voisin][y_voisin]=Status.UNCOVERED
        return True

def afficher_plateau(plateau_jeu:list,plateau_statut:list):
    """
    Hyp: Une fonction qui prend en paramètre le plateau de jeu et le plateau des statuts (couverte, marquée, découverte)
    et qui affiche le plateau actuel dans la console avec des indications pour chaque case selon son statut.
    """
    print(" ", end=' ') 
    print(" ", end=' ')
    for i in range(len(plateau_statut)):
        print(i, end=' ') 
    print()
    for i in range(len(plateau_statut)+2):
        print("_", end='_') 
    print()
    for ligne in range(len(plateau_statut)):
        print(ligne, end=' ')
        print("|", end=' ') 
        for case in range(len(plateau_statut[ligne])):
            if plateau_statut[ligne][case] == Status.COVERED:
                print('C', end=' ')  
            elif plateau_statut[ligne][case] == Status.UNCOVERED:
                print(plateau_jeu[ligne][case],end=' ')  
            elif plateau_statut[ligne][case] == Status.MARK:
                print('M', end=' ')
        print("|", end=' ') 
        print(ligne, end=' ')
        print() #Retour à la ligne
    for i in range(len(plateau_statut)+2):
        print("_", end='_') 
    print()
    print(" ", end=' ') 
    print(" ", end=' ')
    for i in range(len(plateau_statut)):
        print(i, end=' ') 
    print()

    
def decouvre_0(plateau_jeu:list,plateau_statut:list):
    """
    Hyp: Une fonction qui découvre toutes les cases adjacentes qui ont 0 mines autour d'elles, en cascade,
    à partir d'une case donnée, et met à jour le plateau des statuts en conséquence.
    """
    taille:int=len(plateau_jeu)
    action:int=1
    while action!=0:
        action=0
        for ligne in range(len(plateau_statut)):
            for case in range(len(plateau_statut[ligne])):
                if plateau_statut[ligne][case] == Status.UNCOVERED and plateau_jeu[ligne][case] == 0:
                    voisins:list = liste_voisins((ligne,case), taille)
                    for voisin in voisins:
                        x_voisin, y_voisin = voisin
                        if plateau_statut[x_voisin][y_voisin] == Status.COVERED:
                            plateau_statut[x_voisin][y_voisin]=Status.UNCOVERED
                            action+=1

def decouvre_0_recursif(plateau_jeu:list,plateau_statut:list, action:int):
    """
    Hyp: Une fonction qui découvre toutes les cases adjacentes qui ont 0 mines autour d'elles, en cascade,
    à partir d'une case donnée, et met à jour le plateau des statuts en conséquence.
    """
    taille:int=len(plateau_jeu)
    for ligne in range(len(plateau_statut)):
        for case in range(len(plateau_statut[ligne])):
            if plateau_statut[ligne][case] == Status.UNCOVERED and plateau_jeu[ligne][case] == 0:
                voisins:list = liste_voisins((ligne,case), taille)
                for voisin in voisins:
                    x_voisin, y_voisin = voisin
                    if plateau_statut[x_voisin][y_voisin] == Status.COVERED:
                        plateau_statut[x_voisin][y_voisin]=Status.UNCOVERED
                        action=1
    if action==0:
        return None
    return decouvre_0_recursif(plateau_jeu, plateau_statut,0)

def deplacement_joueur(touche: str, position_actuelle: tuple, taille: int) -> tuple:
    """
    Gère le déplacement du joueur en fonction de la touche entrée.
    """
    x, y = position_actuelle
    if touche == 'Z' and x > 0:  
        x -= 1
    elif touche == 'S' and x < taille - 1: 
        x += 1
    elif touche == 'Q' and y > 0:  
        y -= 1
    elif touche == 'D' and y < taille - 1: 
        y += 1
    return (x, y)

def action_joueur(action: str, position_actuelle: tuple, plateau_jeu: list, plateau_statut: list) -> bool:
    """
    Effectue une action sur la case actuelle : miner (découvrir) ou marquer.
    """
    if action == 'miner':
        if not decouvre_case(position_actuelle, plateau_jeu, plateau_statut) and not decouvre_voisin(position_actuelle, plateau_jeu, plateau_statut):
            print("Tu as perdu !")
            return False
    elif action == 'marquer':
        mark_stat(position_actuelle, plateau_jeu, plateau_statut)
    return True


"""
    
    Démarrer le jeu

"""


nb_mines = 3
taille = 5

case_joueur=(1,1)
case_U=liste_voisins(case_joueur, taille)+[case_joueur]

plateau_jeu = init_plateau_mine(taille, nb_mines,case_U)
plateau_statut = init_statut_plateau(taille)

for case in case_U:
    decouvre_case(case, plateau_jeu, plateau_statut)
decouvre_0_recursif(plateau_jeu, plateau_statut, 0)

afficher_plateau(plateau_jeu,plateau_statut)


#afficher_plateau_tkinter(plateau_jeu)

game = True
while game:
    afficher_plateau(plateau_jeu, plateau_statut)
    print(f"Position actuelle du joueur : {case_joueur}")
    print("Utilisez Z (haut), Q (gauche), S (bas), D (droite) pour vous déplacer.")
    print("Tapez 'miner' pour découvrir la case actuelle ou 'marquer' pour poser un drapeau.")

    commande = input("Votre commande : ").strip().upper()

    if commande in ['Z', 'Q', 'S', 'D']:
        case_joueur = deplacement_joueur(commande, case_joueur, taille)
    elif commande in ['MINER', 'MARQUER']:
        if not action_joueur(commande.lower(), case_joueur, plateau_jeu, plateau_statut):
            game = False
    else:
        print("Commande invalide !")

    # Vérification de la condition de victoire
    nb_mark, nb_covered = 0, 0
    for ligne in plateau_statut:
        for case in ligne:
            if case == Status.COVERED:
                nb_covered += 1
            if case == Status.MARK:
                nb_mark += 1
    if nb_covered == nb_mines:
        print("Félicitations, vous avez gagné !")
        game = False


