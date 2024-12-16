from random import randint
from enum import Enum

def init_plateau(taille:int, val:int)->list:
    """
    Description:
    Crée un plateau carré de taille donnée, où chaque case est initialisée à une valeur spécifique.

    Paramètres:
    - taille (int): La taille du plateau (nombre de lignes et de colonnes).
    - val (int): La valeur initiale à placer dans chaque case.

    Retourne:
    - list: Une liste 2D représentant le plateau.
    """
    return [[val for i in range(taille)] for i in range(taille)]

def init_mine(plateau:list, nb_mines:int, case_U:list)->list:
    """
    Description:
    Place aléatoirement un nombre donné de mines sur un plateau, en excluant certaines cases spécifiées.

    Paramètres:
    - plateau (list): Une liste 2D représentant le plateau du jeu.
    - nb_mines (int): Le nombre total de mines à placer.
    - case_U (list): Une liste de tuples représentant les cases interdites (où les mines ne peuvent pas être placées).

    Retourne:
    - list: Une liste de tuples représentant les coordonnées des mines placées.
    """
    taille:int = len(plateau)
    liste_mines:list = []
    while len(liste_mines) < nb_mines:
        y, x = randint(0, taille-1), randint(0, taille-1)
        if (x, y) not in liste_mines and (x, y) not in case_U:
            liste_mines.append((x, y))
    return liste_mines

def liste_voisins(coord:tuple, taille:int)->list:
    """
    Description:
    Renvoie la liste des coordonnées des cases voisines d'une case donnée dans un plateau de taille spécifiée.

    Paramètres:
    - coord (tuple): Les coordonnées (x, y) de la case de départ.
    - taille (int): La taille du plateau (nombre de lignes et colonnes).

    Retourne:
    - list: Une liste de tuples contenant les coordonnées des cases voisines valides.
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
    Description:
    Compte et met à jour le nombre de mines adjacentes pour chaque case non-mine sur un plateau.

    Paramètres:
    - plateau (list): Une liste 2D représentant le plateau du jeu.
    - liste_mines (list): Une liste de tuples contenant les coordonnées des mines.

    Retourne:
    - list: Le plateau mis à jour avec le compte des mines adjacentes pour chaque case.
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
    Description:
    Initialise un plateau de jeu avec des mines et des compteurs de mines adjacentes.

    Paramètres:
    - taille (int): La taille du plateau (nombre de lignes et colonnes).
    - nb_mines (int): Le nombre de mines à placer sur le plateau.
    - case_U (list): Une liste de coordonnées interdites pour le placement des mines.

    Retourne:
    - list: Un plateau 2D avec des mines et des compteurs adjacents.
    """
    plateau = init_plateau(taille, 0)
    liste_mines = init_mine(plateau, nb_mines, case_U)
    for mine in liste_mines:
        x_mine,y_mine=mine[0],mine[1]
        plateau[x_mine][y_mine] = 9
    plateau = init_compte(plateau, liste_mines)
    return plateau

def case_depart(case_joueur,taille):
    """
    Description:
    Corrige les coordonnées d'une case de départ pour qu'elle soit toujours valide dans le plateau.

    Paramètres:
    - case_joueur (list): Les coordonnées initiales de la case de départ.
    - taille (int): La taille du plateau.

    Retourne:
    - list: Les coordonnées corrigées.
    """
    if case_joueur[0]==0:
        case_joueur[0]=1
    if case_joueur[0]==taille:
        case_joueur[0]=taille-1
    if case_joueur[1]==0:
        case_joueur[1]=1
    if case_joueur[1]==taille:
        case_joueur[1]=taille-1
    return case_joueur

class Status(Enum):
    """
    Énumération représentant le statut d'une case sur le plateau.
    """
    COVERED = 1
    UNCOVERED = 2
    MARK = 3

def init_statut_plateau(taille:int)->list:
    """
    Description:
    Initialise un plateau de statuts où toutes les cases sont marquées comme "COVERED".

    Paramètres:
    - taille (int): La taille du plateau (nombre de lignes et colonnes).

    Retourne:
    - list: Un plateau de statuts initialisé.
    """
    return [[Status.COVERED for _ in range(taille)] for _ in range(taille)]

def decouvre_case(coord:tuple,plateau_jeu:list,plateau_statut:list)->bool:
    """
    Description:
    Découvre une case du plateau de jeu et met à jour le statut correspondant.

    Paramètres:
    - coord (tuple): Les coordonnées de la case à découvrir.
    - plateau_jeu (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - bool: Vrai si la case découverte n'est pas une mine, Faux sinon.
    """
    plateau_statut[coord[0]][coord[1]]=Status.UNCOVERED
    if plateau_jeu[coord[0]][coord[1]]!=9:
        return True
    return False

def mark_stat(coord:tuple,plateau_jeu:list,plateau_statut:list):
    """
    Description:
    Marque ou démarque une case sur le plateau de statuts en fonction de son statut actuel.

    Paramètres:
    - coord (tuple): Les coordonnées de la case à (dé)marquer.
    - plateau_jeu (list): Le plateau de jeu.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - None
    """
    if plateau_statut[coord[0]][coord[1]]==Status.MARK:
        plateau_statut[coord[0]][coord[1]]=Status.COVERED
    else: 
        plateau_statut[coord[0]][coord[1]]=Status.MARK
        
def nb_voisin_MARK(coord:tuple,plateau_statut:list)->int:
    """
    Description:
    Compte le nombre de cases marquées autour d'une case donnée.

    Paramètres:
    - coord (tuple): Les coordonnées de la case cible.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - int: Le nombre de cases marquées autour de la case cible.
    """
    nb=0
    taille=len(plateau_statut)
    voisins = liste_voisins(coord, taille)
    for voisin in voisins:
        x_voisin, y_voisin = voisin
        if plateau_statut[x_voisin][y_voisin]==Status.MARK:
            nb+=1
    return nb

def decouvre_0_recursif(plateau_jeu:list,plateau_statut:list, action:int):
    """
    Description:
    Découvre de manière récursive toutes les cases adjacentes ayant 0 mines autour d'elles.

    Paramètres:
    - plateau_jeu (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau des statuts des cases.
    - action (int): Indicateur de continuation de l'action (0 pour arrêter).

    Retourne:
    - None
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

def robot_action_simple(plateau:list, plateau_statut:list):
    """
    Description:
    Applique une stratégie simple pour découvrir ou marquer des cases en fonction des informations disponibles.

    Paramètres:
    - plateau (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - None
    """
    case_marquer=[]
    action=1
    while action!=0:
        action=0
        for x in range(len(plateau)):
            for y in range(len(plateau[0])):
                
                if plateau_statut[x][y] == Status.UNCOVERED: 
                    nb_mines_adjacentes = plateau[x][y]  
                    voisins = liste_voisins((x, y), len(plateau))  
                    
                    cases_couvertes = [v for v in voisins if plateau_statut[v[0]][v[1]] != Status.UNCOVERED]
                    cases_marquees = [v for v in voisins if plateau_statut[v[0]][v[1]] == Status.MARK]
                    
                    if len(cases_couvertes) == nb_mines_adjacentes:
                        for case in cases_couvertes:
                            if case not in case_marquer:
                                plateau_statut[case[0]][case[1]]=Status.MARK
                                action+=1
                                case_marquer.append(case)
    
                    
                    elif len(cases_marquees) == nb_mines_adjacentes:
                        for case in voisins:
                            if case not in case_marquer and case not in cases_marquees:
                                decouvre_case(case, plateau, plateau_statut)
                                action+=1
                                
def robot_action_complexe(plateau:list, plateau_statut:list):
    """
    Description:
    Parcourt tout le plateau et vérifie chaque case découverte pour appliquer une logique avancée.

    Paramètres:
    - plateau (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - None
    """
    for x in range(len(plateau)):
        for y in range(len(plateau[0])):
            if plateau_statut[x][y] == Status.UNCOVERED:
                verifier_case([x, y], plateau, plateau_statut)

def verifier_case(case_A:list, plateau:list, plateau_statut:list):
    """
    Description:
    Vérifie une case découverte et prépare les données nécessaires pour des calculs plus complexes.

    Paramètres:
    - case_A (list): Les coordonnées de la case à vérifier.
    - plateau (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - None
    """
    couvertes = [voisin for voisin in liste_voisins(case_A, len(plateau)) 
                 if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    
    uncovered_voisins = voisin_voisin(case_A,couvertes, plateau, plateau_statut)
    
    calcul(case_A, couvertes, uncovered_voisins, plateau, plateau_statut)

def voisin_voisin(case_A:list,couvertes:list, plateau:list, plateau_statut:list):
    """
    Description:
    Retourne toutes les cases découvertes autour des cases couvertes spécifiées.

    Paramètres:
    - case_A (list): Les coordonnées de la case de référence.
    - couvertes (list): La liste des cases couvertes à vérifier.
    - plateau (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau des statuts des cases.

    Retourne:
    - list: Une liste de cases découvertes.
    """
    uncovered_voisins = []
    for case in couvertes:
        voisins = liste_voisins(case, len(plateau))
        uncovered_voisins += [voisin for voisin in voisins 
                              if plateau_statut[voisin[0]][voisin[1]] == Status.UNCOVERED and [voisin[0],voisin[1]]!=[case_A[0],case_A[1]]]
    return uncovered_voisins

def voisin_commun(case_A:list, case_B:list, plateau_statut:list):
    """
    Description:
    Retourne la liste des cases couvertes communes entre les voisins de case_A et case_B.

    Paramètres:
    - case_A (list): Les coordonnées de la première case.
    - case_B (list): Les coordonnées de la seconde case.
    - plateau_statut (list): Le plateau contenant les statuts des cases.

    Retourne:
    - list: Une liste des cases couvertes communes entre les voisins de case_A et case_B.
    """
    voisins_A = [voisin for voisin in liste_voisins(case_A, len(plateau_statut)) 
                 if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    voisins_B = [voisin for voisin in liste_voisins(case_B, len(plateau_statut)) 
                 if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    return list(set(voisins_A) & set(voisins_B))  # Intersection des deux listes

def calcul(case_A:list, couvertes:list, uncovered_voisins:list, plateau:list, plateau_statut:list):
    """
    Description:
    Applique la logique complexe en comparant case_A avec ses voisins uncovered (caseB).

    Paramètres:
    - case_A (list): Les coordonnées de la case cible.
    - couvertes (list): Les cases couvertes autour de case_A.
    - uncovered_voisins (list): Les cases découvertes autour des cases couvertes.
    - plateau (list): Le plateau de jeu contenant les valeurs des cases.
    - plateau_statut (list): Le plateau contenant les statuts des cases.

    Retourne:
    - None
    """
    nb_mines_adj_A = plateau[case_A[0]][case_A[1]]
    nb_mark_adj_A = sum(1 for voisin in liste_voisins(case_A, len(plateau)) 
                        if plateau_statut[voisin[0]][voisin[1]] == Status.MARK)

    for case_B in uncovered_voisins:
        nb_mark_adj_B = sum(1 for voisin in liste_voisins(case_B, len(plateau)) 
                            if plateau_statut[voisin[0]][voisin[1]] == Status.MARK)
        
        # Nombre de mines adjacentes à case_B
        nb_mines_adj_B = plateau[case_B[0]][case_B[1]]
        
        # Nombre de cases couvertes autour de case_B
        voisins_B = [voisin for voisin in liste_voisins(case_B, len(plateau_statut)) 
                     if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
        nb_case_covered_B = len(voisins_B)
        
        # Cases couvertes communes entre case_A et case_B
        voisins_communs = voisin_commun(case_A, case_B, plateau_statut)
        nb_voisin_commun_AB = len(voisins_communs)
        
        # Calcul du résultat
        resultat = (nb_mines_adj_B - nb_mark_adj_B) - (nb_case_covered_B - nb_voisin_commun_AB)
        
        if resultat == (nb_mines_adj_A - nb_mark_adj_A) :
            # Découvrir toutes les cases autour de case_A sauf les voisins communs
            voisins_A = [voisin for voisin in liste_voisins(case_A, len(plateau_statut)) 
                         if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
            for case in voisins_A:
                if case not in voisins_communs:
                    decouvre_case((case[0],case[1]), plateau, plateau_statut)
        if nb_case_covered_B==nb_voisin_commun_AB:
            mark_complexe(case_A, case_B, nb_mines_adj_A, nb_voisin_commun_AB, resultat, nb_mark_adj_A, plateau, plateau_statut)
        
def mark_complexe(case_A:list, case_B:list, nb_mines_adj_A:int, nb_voisin_commun_AB:int, resultat:int, nb_mark_adj_A:int, plateau:list, plateau_statut:list):
    """
    Description:
    Traite les cas où le résultat n'est pas égal à 0.
    Effectue un calcul spécifique et marque les cases si la condition est remplie.

    Paramètres:
    - case_A (list): Les coordonnées de la première case.
    - case_B (list): Les coordonnées de la seconde case.
    - nb_mines_adj_A (int): Le nombre de mines adjacentes à case_A.
    - nb_voisin_commun_AB (int): Le nombre de voisins communs entre case_A et case_B.
    - resultat (int): Le résultat du calcul complexe.
    - nb_mark_adj_A (int): Le nombre de cases marquées autour de case_A.
    - plateau (list): Le plateau de jeu.
    - plateau_statut (list): Le plateau contenant les statuts des cases.

    Retourne:
    - None
    """
    voisins_A = [voisin for voisin in liste_voisins(case_A, len(plateau_statut)) 
                 if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    nb_voisin_covered_A=len(voisins_A)
    
    calcul = nb_mines_adj_A - nb_mark_adj_A - resultat

    if calcul ==  (nb_voisin_covered_A - nb_voisin_commun_AB):
        voisins_communs = voisin_commun(case_A, case_B, plateau_statut)
        for case in voisins_A:
            if case not in voisins_communs:
                mark_stat((case[0],case[1]), plateau, plateau_statut)

def plateau_jeu_possible_difficile(taille, nb_mines, case_joueur):
    """
    Description:
    Génère un plateau de jeu jouable avec une configuration valide de mines et de cases découvertes.

    Paramètres:
    - taille (int): La taille du plateau.
    - nb_mines (int): Le nombre de mines à placer.
    - case_joueur (list): Les coordonnées initiales de la case sélectionnée par le joueur.

    Retourne:
    - list: Le plateau de jeu configuré.
    """
    jeu_possible=False
    j=0
    while not jeu_possible:
        j+=1
        case_joueur=case_depart(case_joueur, taille)
        case_U=liste_voisins(case_joueur, taille)+[(case_joueur[0],case_joueur[1])]
        plateau_jeu = init_plateau_mine(taille, nb_mines,case_U)
        plateau_statut = init_statut_plateau(taille)
        
        for case in case_U:
            decouvre_case(case, plateau_jeu, plateau_statut)
        decouvre_0_recursif(plateau_jeu, plateau_statut, 0)
        
        robot_action_simple(plateau_jeu, plateau_statut)
        
        robot_action_complexe(plateau_jeu, plateau_statut)
        game=True
        while game:
            plateau_statut_pred=plateau_statut
            robot_action_simple(plateau_jeu, plateau_statut)
            robot_action_complexe(plateau_jeu, plateau_statut)
            decouvre_0_recursif(plateau_jeu,plateau_statut,0)
            nb_uncovered=0
            for ligne in range(len(plateau_statut)):
                for case in range(len(plateau_statut[ligne])):
                    if plateau_statut[ligne][case] == Status.UNCOVERED:
                        nb_uncovered+=1
            if nb_uncovered==(taille**2)-nb_mines :
                print("win dure")
                jeu_possible=True
                game=False
            elif plateau_statut_pred==plateau_statut:
                game=False
    return plateau_jeu

def plateau_jeu_possible_facil(taille, nb_mines, case_joueur):
    """
    Description:
    Génère un plateau de jeu avec une configuration simplifiée pour réussir automatiquement dans un mode facile.

    Paramètres:
    - taille (int): La taille du plateau.
    - nb_mines (int): Le nombre de mines à placer.
    - case_joueur (list): Les coordonnées initiales de la case sélectionnée par le joueur.

    Retourne:
    - list: Le plateau de jeu configuré.
    """
    jeu_possible=False
    while not jeu_possible:
        case_joueur=case_depart(case_joueur, taille)
        case_U=liste_voisins(case_joueur, taille)+[(case_joueur[0],case_joueur[1])]
        plateau_jeu = init_plateau_mine(taille, nb_mines,case_U)
        plateau_statut = init_statut_plateau(taille)
        
        for case in case_U:
            decouvre_case(case, plateau_jeu, plateau_statut)
        decouvre_0_recursif(plateau_jeu, plateau_statut, 0)
        
        robot_action_simple(plateau_jeu, plateau_statut)
        nb_uncovered=0
        for ligne in range(len(plateau_statut)):
            for case in range(len(plateau_statut[ligne])):
                if plateau_statut[ligne][case] == Status.UNCOVERED:
                    nb_uncovered+=1
        if nb_uncovered==(taille**2)-nb_mines :
            jeu_possible=True
    return plateau_jeu
