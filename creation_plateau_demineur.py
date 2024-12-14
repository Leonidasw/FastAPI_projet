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

def case_depart(case_joueur: list, taille: int) -> list:
    """
    Déplace la case de départ pour s'assurer qu'elle reste dans les limites du plateau.

    Arguments :
    - case_joueur (list[int]) : Coordonnées de la case choisie par le joueur (ex : [x, y]).
    - taille (int) : Taille du plateau.

    Retour :
    - list[int] : Coordonnées ajustées de la case de départ.
    """
    if case_joueur[0] == 0:
        case_joueur[0] = 1
    if case_joueur[0] == taille:
        case_joueur[0] = taille - 1
    if case_joueur[1] == 0:
        case_joueur[1] = 1
    if case_joueur[1] == taille:
        case_joueur[1] = taille - 1
    return case_joueur
    

class Status(Enum):
    COVERED = 1
    UNCOVERED = 2
    MARK = 3

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
    
def case_depart(case_joueur: list, taille: int) -> list:
    """
    Déplace la case de départ pour s'assurer qu'elle reste dans les limites du plateau.

    Arguments :
    - case_joueur (list[int]) : Coordonnées de la case choisie par le joueur (ex : [x, y]).
    - taille (int) : Taille du plateau.

    Retour :
    - list[int] : Coordonnées ajustées de la case de départ.
    """
    if case_joueur[0] == 0:
        case_joueur[0] = 1
    if case_joueur[0] == taille:
        case_joueur[0] = taille - 1
    if case_joueur[1] == 0:
        case_joueur[1] = 1
    if case_joueur[1] == taille:
        case_joueur[1] = taille - 1
    return case_joueur


def decouvre_0(plateau_jeu: list, plateau_statut: list) -> None:
    """
    Découvre toutes les cases adjacentes ayant 0 mines autour d'elles, en cascade,
    en mettant à jour le plateau des statuts.

    Arguments :
    - plateau_jeu (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut (COVERED, UNCOVERED, MARK) des cases.

    Retour :
    - None : Modifie le plateau_statut directement.
    """
    taille: int = len(plateau_jeu)
    action: int = 1
    while action != 0:
        action = 0
        for ligne in range(len(plateau_statut)):
            for case in range(len(plateau_statut[ligne])):
                if plateau_statut[ligne][case] == Status.UNCOVERED and plateau_jeu[ligne][case] == 0:
                    voisins: list = liste_voisins((ligne, case), taille)
                    for voisin in voisins:
                        x_voisin, y_voisin = voisin
                        if plateau_statut[x_voisin][y_voisin] == Status.COVERED:
                            plateau_statut[x_voisin][y_voisin] = Status.UNCOVERED
                            action += 1


def decouvre_0_recursif(plateau_jeu: list, plateau_statut: list, action: int) -> None:
    """
    Découvre les cases adjacentes ayant 0 mines autour d'elles de manière récursive.

    Arguments :
    - plateau_jeu (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.
    - action (int) : Indicateur de continuation des découvertes.

    Retour :
    - None : Modifie le plateau_statut directement.
    """
    taille: int = len(plateau_jeu)
    for ligne in range(len(plateau_statut)):
        for case in range(len(plateau_statut[ligne])):
            if plateau_statut[ligne][case] == Status.UNCOVERED and plateau_jeu[ligne][case] == 0:
                voisins: list = liste_voisins((ligne, case), taille)
                for voisin in voisins:
                    x_voisin, y_voisin = voisin
                    if plateau_statut[x_voisin][y_voisin] == Status.COVERED:
                        plateau_statut[x_voisin][y_voisin] = Status.UNCOVERED
                        action = 1
    if action == 0:
        return None
    return decouvre_0_recursif(plateau_jeu, plateau_statut, 0)


def robot_action_simple(plateau: list, plateau_statut: list) -> None:
    """
    Applique une stratégie simple pour découvrir ou marquer les cases.

    Arguments :
    - plateau (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - None : Modifie directement les plateaux.
    """
    case_marquer: list = []
    action: int = 1
    while action != 0:
        action = 0
        for x in range(len(plateau)):
            for y in range(len(plateau[0])):
                if plateau_statut[x][y] == Status.UNCOVERED:
                    nb_mines_adjacentes: int = plateau[x][y]
                    voisins: list = liste_voisins((x, y), len(plateau))

                    cases_couvertes: list = [v for v in voisins if plateau_statut[v[0]][v[1]] == Status.COVERED]
                    cases_marquees: list = [v for v in voisins if plateau_statut[v[0]][v[1]] == Status.MARK]

                    if len(cases_couvertes) == nb_mines_adjacentes:
                        for case in cases_couvertes:
                            if case not in case_marquer:
                                plateau_statut[case[0]][case[1]] = Status.MARK
                                action += 1
                                case_marquer.append(case)

                    elif len(cases_marquees) == nb_mines_adjacentes:
                        for case in cases_couvertes:
                            decouvre_case(case, plateau, plateau_statut)
                            action += 1


def mark_complex(case_A: list, case_B: list, nb_mines_adj_A: int, nb_voisin_commun_AB: int, resultat: int, nb_mark_adj_A: int, plateau: list, plateau_statut: list) -> None:
    """
    Marque les cases dans des scénarios complexes selon les voisins communs.

    Arguments :
    - case_A (list[int]) : Coordonnées de la première case (ex : [x, y]).
    - case_B (list[int]) : Coordonnées de la deuxième case (ex : [x, y]).
    - nb_mines_adj_A (int) : Nombre de mines adjacentes à la case A.
    - nb_voisin_commun_AB (int) : Nombre de voisins communs entre A et B.
    - resultat (int) : Différence entre les nombres de mines et de cases couvertes.
    - nb_mark_adj_A (int) : Nombre de cases marquées adjacentes à la case A.
    - plateau (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - None : Marque les cases pertinentes directement.
    """
    voisins_A: list = [voisin for voisin in liste_voisins(case_A, len(plateau_statut))
                      if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    nb_voisin_covered_A: int = len(voisins_A)

    calcul: int = nb_mines_adj_A - nb_mark_adj_A - resultat

    if calcul == (nb_voisin_covered_A - nb_voisin_commun_AB):
        voisins_communs: list = voisin_commun(case_A, case_B, plateau_statut)
        for case in voisins_A:
            if case not in voisins_communs:
                mark_stat((case[0], case[1]), plateau, plateau_statut)


def robot_action_complexe(plateau: list, plateau_statut: list) -> None:
    """
    Applique une logique avancée pour analyser les cases découvertes (UNCOVERED) et
    déduire des informations sur les cases couvertes adjacentes.

    Arguments :
    - plateau (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - None : Modifie directement les plateaux.
    """
    for x in range(len(plateau)):
        for y in range(len(plateau[0])):
            if plateau_statut[x][y] == Status.UNCOVERED:
                verifier_case([x, y], plateau, plateau_statut)


def verifier_case(case_A: list, plateau: list, plateau_statut: list) -> None:
    """
    Vérifie une case découverte et prépare les données nécessaires pour des calculs complexes.

    Arguments :
    - case_A (list[int]) : Coordonnées de la case à vérifier (ex : [x, y]).
    - plateau (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - None : Appelle des fonctions pour marquer ou découvrir des cases selon la logique.
    """
    couvertes: list = [voisin for voisin in liste_voisins(case_A, len(plateau))
                      if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    uncovered_voisins: list = voisin_voisin(case_A, couvertes, plateau, plateau_statut)
    calcul(case_A, couvertes, uncovered_voisins, plateau, plateau_statut)


def voisin_voisin(case_A: list, couvertes: list, plateau: list, plateau_statut: list) -> list:
    """
    Identifie les voisins découverts (UNCOVERED) des cases couvertes autour d'une case donnée.

    Arguments :
    - case_A (list[int]) : Coordonnées de la case d'origine (ex : [x, y]).
    - couvertes (list[list[int]]) : Liste des cases couvertes adjacentes.
    - plateau (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - list[list[int]] : Liste des cases découvertes adjacentes.
    """
    uncovered_voisins: list = []
    for case in couvertes:
        voisins: list = liste_voisins(case, len(plateau))
        uncovered_voisins += [voisin for voisin in voisins
                              if plateau_statut[voisin[0]][voisin[1]] == Status.UNCOVERED and voisin != case_A]
    return uncovered_voisins


def calcul(case_A: list, couvertes: list, uncovered_voisins: list, plateau: list, plateau_statut: list) -> None:
    """
    Applique la logique complexe en comparant une case donnée (case_A) avec ses voisins.

    Arguments :
    - case_A (list[int]) : Coordonnées de la case à analyser (ex : [x, y]).
    - couvertes (list[list[int]]) : Liste des cases couvertes autour de case_A.
    - uncovered_voisins (list[list[int]]) : Liste des cases découvertes autour de case_A.
    - plateau (list[list[int]]) : Plateau contenant les informations sur les mines et le compte des voisins.
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - None : Modifie les plateaux directement en marquant ou découvrant des cases.
    """
    nb_mines_adj_A: int = plateau[case_A[0]][case_A[1]]
    nb_mark_adj_A: int = sum(1 for voisin in liste_voisins(case_A, len(plateau))
                            if plateau_statut[voisin[0]][voisin[1]] == Status.MARK)

    for case_B in uncovered_voisins:
        nb_mark_adj_B: int = sum(1 for voisin in liste_voisins(case_B, len(plateau))
                                if plateau_statut[voisin[0]][voisin[1]] == Status.MARK)

        nb_mines_adj_B: int = plateau[case_B[0]][case_B[1]]

        voisins_B: list = [voisin for voisin in liste_voisins(case_B, len(plateau_statut))
                          if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
        nb_case_covered_B: int = len(voisins_B)

        voisins_communs: list = voisin_commun(case_A, case_B, plateau_statut)
        nb_voisin_commun_AB: int = len(voisins_communs)

        resultat: int = (nb_mines_adj_B - nb_mark_adj_B) - (nb_case_covered_B - nb_voisin_commun_AB)

        if resultat == (nb_mines_adj_A - nb_mark_adj_A):
            voisins_A: list = [voisin for voisin in liste_voisins(case_A, len(plateau_statut))
                              if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
            for case in voisins_A:
                if case not in voisins_communs:
                    decouvre_case((case[0], case[1]), plateau, plateau_statut)


def voisin_commun(case_A: list, case_B: list, plateau_statut: list) -> list:
    """
    Identifie les voisins communs couverts entre deux cases données.

    Arguments :
    - case_A (list[int]) : Coordonnées de la première case (ex : [x, y]).
    - case_B (list[int]) : Coordonnées de la deuxième case (ex : [x, y]).
    - plateau_statut (list[list[Status]]) : Plateau indiquant le statut des cases.

    Retour :
    - list[list[int]] : Liste des cases couvertes communes.
    """
    voisins_A: list = [voisin for voisin in liste_voisins(case_A, len(plateau_statut))
                      if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    voisins_B: list = [voisin for voisin in liste_voisins(case_B, len(plateau_statut))
                      if plateau_statut[voisin[0]][voisin[1]] == Status.COVERED]
    return list(set(voisins_A) & set(voisins_B))


def plateau_jeu_possible(nb_mines: int, taille: int, case_joueur: list) -> list:
    """
    Génère un plateau de jeu valide en s'assurant qu'il est jouable et respecte les règles du démineur.

    Arguments :
    - nb_mines (int) : Nombre de mines à placer sur le plateau.
    - taille (int) : Taille du plateau de jeu (carré).
    - case_joueur (list[int]) : Coordonnées initiales choisies par le joueur.

    Retour :
    - list[list[int]] : Plateau de jeu avec les mines placées.
    """
    jeu_possible: bool = False
    while not jeu_possible:
        case_joueur = case_depart(case_joueur, taille)
        case_U: list = liste_voisins(case_joueur, taille) + [case_joueur]
        plateau_jeu: list = init_plateau_mine(taille, nb_mines, case_U)
        plateau_statut: list = init_statut_plateau(taille)
        
        for case in case_U:
            decouvre_case(case, plateau_jeu, plateau_statut)
        decouvre_0_recursif(plateau_jeu, plateau_statut, 0)

        robot_action_simple(plateau_jeu, plateau_statut)
        robot_action_complexe(plateau_jeu, plateau_statut)

        i: int = 0
        game: bool = True
        while game:
            robot_action_simple(plateau_jeu, plateau_statut)
            robot_action_complexe(plateau_jeu, plateau_statut)
            decouvre_0_recursif(plateau_jeu, plateau_statut, 0)

            nb_mark: int = 0
            nb_covered: int = 0
            for ligne in range(len(plateau_statut)):
                for case in range(len(plateau_statut[ligne])):
                    if plateau_statut[ligne][case] == Status.COVERED:
                        nb_covered += 1
                    if plateau_statut[ligne][case] == Status.MARK:
                        nb_mark += 1

            i += 1
            if nb_mark == nb_mines and nb_covered == 0:
                jeu_possible = True
                game = False
            elif i == (taille**2)*1.1:
                game = False

    return plateau_jeu
