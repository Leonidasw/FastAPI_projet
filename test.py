import uvicorn
from fastapi import Form, Response
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect # import de la classe FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from hashlib import sha256
from contextlib import asynccontextmanager
import sqlite3
import os

dbpath = os.path.join(os.path.dirname(__file__), "db", "database2.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ouvrir la connexion SQLite au démarrage de l'application
    connection = sqlite3.connect(dbpath)
    cursor = connection.cursor()

    # Exécuter le script SQL uniquement si les tables n'existent pas déjà
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
    """)
    if not cursor.fetchone():  # Si aucune table "users" n'est trouvée, exécuter le script
        with open("db/BD_Table.sql", "r") as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        connection.commit()

    # Fournir la connexion à l'application via le contexte
    yield {"connection": connection, "cursor": cursor}

    # Fermer la connexion proprement à l'arrêt de l'application
    connection.close()



templates = Jinja2Templates(directory="templates/")
app = FastAPI(lifespan=lifespan) # Création de l application

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return RedirectResponse(url="/login")

def verif_mdp(username:str,mdp:str)->bool:
    """
    Hyp: Vérifie que le coupe username et mot de passe est correcte. Return True si le couple est bon sinon false
    """
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        db_mdp = cur.execute(f"SELECT user_mdp FROM Joueur WHERE user_pseudo=='{username}'").fetchone()
    if db_mdp is None:
        return False
    return mdp==db_mdp[0]

@app.post("/soumettre_login", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Hyp: Récupère les données fourni par l'utilisateur, et le connecte si le couple username et mdp est correct.
    """
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        data = cur.execute(f"SELECT * FROM Joueur WHERE user_pseudo=='{username}'").fetchone()
    ### Vérification du mot de passe ####
    if data is None:
        return templates.TemplateResponse('login.html',{'request': request,'Valide':"Le nom d'utilisateur n'existe pas!"}) 
    mdp= sha256(password.encode('utf-8')).hexdigest()
    if verif_mdp(username,mdp):
        response = RedirectResponse(url="/profile_page",status_code=303)
        response.set_cookie(key="username", value=username)
        response.set_cookie(key="password", value=mdp)
        return response
    return templates.TemplateResponse('login.html',{'request': request,'Valide':"Le mot de passe n'est pas bon!"})

@app.get("/logout")
async def logout(response:Response):
    """
    Hyp: Pour se déconnecter du site (cela supprimme les cookies)
    """
    response = RedirectResponse(url="/login")
    response.delete_cookie("username")
    response.delete_cookie("password")
    response.delete_cookie("difficulty")
    return response

@app.get("/login")
async def login(request:Request):
    """
    Hyp: Pour aller sur le login.html quand on va sur /html, vérifie s'il n'est pas déjà login, si oui il le redirige dans profile_page
    """
    username = request.cookies.get("username")
    if username is None:
        return templates.TemplateResponse('login.html',{'request': request,'title':'Login page',})
    return RedirectResponse(url="/profile_page")
    

@app.get("/inscription")
async def inscription(request:Request):
    """
    Hyp: Pour aller sur le inscription.html quand on va sur /inscription, vérifie s'il n'est pas déjà login, si oui il le redirige dans profile_page
    """
    username = request.cookies.get("username")
    if username is not None:
        return RedirectResponse(url="/profile_page")
    return templates.TemplateResponse('inscription.html',{'request': request,'title':'Inscription page',})

@app.get("/profile_page")
async def profile_page(request:Request):
    """
    Hyp: Pour aller sur le profile_page.html quand on va sur /profile_page, vérifie s'il est login, si il n'est pas connecté le redirige vers /login
    """
    username = request.cookies.get("username")
    if username is None:
        return RedirectResponse(url="/login")
    mdp= request.cookies.get("password")
    if verif_mdp(username,mdp) is False: ## Vérifie si quelqu'un à modifier le cookie username pour usurper l'identité de quelqu'un d'autre.
        return templates.TemplateResponse(
                    "error.html", 
                    {"request": request, "message":"ERREUR GRAVE: Le nom d'utilisateur et le mot de passe ne correspond pas à la base de données!"})     
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
    jeux=cur.execute(f"SELECT COUNT(*) FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{username}';").fetchone()[0]
    temps = cur.execute(f"SELECT MIN(Score.score_centiseconds) FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{username}';").fetchone()[0]
    if temps is None:
        return templates.TemplateResponse(
                "profile_page.html", 
                {"request": request, "username": username,"games":jeux,"time":'None'})
    else:
        minutes = int(temps) // 6000
        seconds = (int(temps) % 6000) // 100
        centis = int(temps) % 100

        # Format each component with leading zero if necessary

        return templates.TemplateResponse(
                    "profile_page.html", 
                    {"request": request, "username": username,"games":jeux,"time":f'{minutes} minutes, {seconds} secondes et {centis} centisecondes'})       

@app.post("/soumettre_register", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Hyp: Récupère les données fourni par l'utilisateur, et crée le compte et l'insère dans la bdd si l'utilisateur n'est pas déjà utilisé
    """
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        test_user = cur.execute(f"SELECT * FROM Joueur WHERE user_pseudo=='{username}'   ").fetchone()
        password=sha256(password.encode('utf-8')).hexdigest()
        if test_user is None:
            cur.execute(f"INSERT INTO Joueur(user_pseudo, user_mdp) VALUES('{username}','{password}')").fetchone()
            response =  RedirectResponse(url="/profile_page",status_code=303)
            response.set_cookie(key="username", value=username)
            response.set_cookie(key="password", value=password)
            return response
        return templates.TemplateResponse('inscription.html',{'request': request,'Valide':"Le nom d'utilisateur est déjà utilisé"})
    
@app.get("/demineur")
async def demineur():
    """
    Hyp: Redirige l'utilisateur vers /demineur/facile
    """
    return RedirectResponse(url="/demineur/facile",status_code=303)

@app.get('/leaderboard')
async def leaderboard(request:Request):
    """
    Hyp: Récupère les données des utilisateurs dans la bdd et l'affiche dans plusieurs tableaux
    """
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        data_facile = cur.execute('SELECT Joueur.user_pseudo,Score.score_centiseconds,Score.date_jeu FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Score.difficulte_jeu=="facile" AND Score.custom == "NULL" ORDER BY Score.score_centiseconds ASC LIMIT 5').fetchall()
        data_medium = cur.execute('SELECT Joueur.user_pseudo,Score.score_centiseconds,Score.date_jeu FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Score.difficulte_jeu=="moyen" AND Score.custom == "NULL" ORDER BY Score.score_centiseconds ASC LIMIT 5').fetchall()
        data_difficile = cur.execute('SELECT Joueur.user_pseudo,Score.score_centiseconds,Score.date_jeu FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Score.difficulte_jeu=="difficile" AND Score.custom == "NULL" ORDER BY Score.score_centiseconds ASC LIMIT 5').fetchall()
        wins = cur.execute("SELECT Joueur.user_pseudo, COUNT(Score.id_user) AS appearances FROM Score JOIN Joueur ON Score.id_user = Joueur.id_user GROUP BY Joueur.user_pseudo ORDER BY appearances DESC;").fetchall()#WHERE Score.custom == 1
        custom_rank = cur.execute('SELECT Joueur.user_pseudo,Score.score_centiseconds,Score.date_jeu,Champ.id_champ,Champ.difficulte FROM Score JOIN Joueur ON Joueur.id_user=Score.id_user JOIN Champ ON Joueur.id_user = Champ.user_id WHERE Score.custom != "NULL" AND Score.custom=Champ.id_champ ORDER BY Score.score_centiseconds ASC LIMIT 5').fetchall()
    return templates.TemplateResponse(
        'leaderboard.html',
        {
            'request': request,
            'title': "Classements",
            'score_facile': data_facile,
            'score_medium': data_medium,
            'score_difficile': data_difficile,
            'wins':wins,
            'custom':custom_rank,
            'enumerate': enumerate  # Add `enumerate` to the template context
        }
    )

@app.get('/custom_create')
async def create_board(request:Request):
    """
    Hyp: Pour aller sur le custom_create.html quand on va sur /custom_create, vérifie s'il est login, si il n'est pas connecté le redirige vers /login
    """
    username = request.cookies.get("username")
    if username is None:  # Vérifie si il est connecté
        return RedirectResponse(url="/login")
    mdp= request.cookies.get("password")
    if verif_mdp(username,mdp) is False: ## Vérifie si quelqu'un à modifier le cookie username pour usurper l'identité de quelqu'un d'autre.
        return templates.TemplateResponse(
                    "error.html", 
                    {"request": request, "message":"ERREUR GRAVE: Le nom d'utilisateur et le mot de passe ne correspond pas à la base de données!"})
    return templates.TemplateResponse(
        "custom_create.html", 
        {"request": request})  

@app.get("/demineur/facile")
async def demineur_facile(request:Request):
    """
    Hyp: Affiche le jeu en mode facile.
    """
    username = request.cookies.get("username")
    if username is None:
        response =templates.TemplateResponse(
            'demineur.html',
            {
                'request':request,
                'difficulty':"facile",
                'inscrit': "Vous n'êtes pas inscrit"
            }
        )
        response.set_cookie(key="difficulty", value="facile")
        return response
    mdp= request.cookies.get("password")
    if verif_mdp(username,mdp) is False: ## Vérifie si quelqu'un à modifier le cookie username pour usurper l'identité de quelqu'un d'autre.
        return templates.TemplateResponse(
                    "error.html", 
                    {"request": request, "message":"ERREUR GRAVE: Le nom d'utilisateur et le mot de passe ne correspond pas à la base de données!"})
    response =templates.TemplateResponse(
            'demineur.html',
            {
                'request':request,
                'difficulty':"facile",
                'inscrit': f"Vous êtes inscrit comme {username}"
            }
    )
    response.set_cookie(key="difficulty", value="facile")
    return response

@app.get("/demineur/moyen")
async def demineur_moyen(request:Request):
    """
    Hyp: Affiche le jeu en mode moyen.
    """
    username = request.cookies.get("username")
    if username is None:
        response =templates.TemplateResponse(
            'demineur.html',
            {
                'request':request,
                'difficulty':"moyen",
                'inscrit': "Vous n'êtes pas inscrit"
            }
        )
        response.set_cookie(key="difficulty", value="moyen")
        return response
    mdp= request.cookies.get("password")
    if verif_mdp(username,mdp) is False: ## Vérifie si quelqu'un à modifier le cookie username pour usurper l'identité de quelqu'un d'autre.
        return templates.TemplateResponse(
                    "error.html", 
                    {"request": request, "message":"ERREUR GRAVE: Le nom d'utilisateur et le mot de passe ne correspond pas à la base de données!"})
    response =templates.TemplateResponse(
            'demineur.html',
            {
                'request':request,
                'difficulty':"moyen",
                'inscrit': f"Vous êtes inscrit comme {username}"
            }
    )
    response.set_cookie(key="difficulty", value="moyen")
    return response


@app.get("/demineur/difficile")
async def demineur_difficile(request:Request):
    """
    Hyp: Affiche le jeu en mode difficile.
    """
    username = request.cookies.get("username")
    if username is None:
        response =templates.TemplateResponse(
            'demineur.html',
            {
                'request':request,
                'difficulty':"difficile",
                'inscrit': "Vous n'êtes pas inscrit"
            }
        )
        response.set_cookie(key="difficulty", value="difficile")
        return response
    mdp= request.cookies.get("password")
    if verif_mdp(username,mdp) is False: ## Vérifie si quelqu'un à modifier le cookie username pour usurper l'identité de quelqu'un d'autre.
        return templates.TemplateResponse(
                    "error.html", 
                    {"request": request, "message":"ERREUR GRAVE: Le nom d'utilisateur et le mot de passe ne correspond pas à la base de données!"})
    response =templates.TemplateResponse(
            'demineur.html',
            {
                'request':request,
                'difficulty':"difficile",
                'inscrit': f"Vous êtes inscrit comme {username}"
            }
    )
    response.set_cookie(key="difficulty", value="difficile")
    return response

from pydantic import BaseModel
class Score(BaseModel): #Permet de récupéré les données de js.
    score: int

@app.post("/demineur/score")
async def score(request:Request):
    """
    Hyp: Après une demande du code java script, enrengistre le score fourni par java script dans la bdd 
    """
    username=request.cookies.get("username")
    difficulty=request.cookies.get("difficulty")
    data = await request.json()
    score_centiseconds = data["score"]
    if score_centiseconds <= 0:
        return 
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        id_user=cur.execute(f"SELECT id_user FROM Joueur WHERE user_pseudo=='{username}'").fetchone()[0]
        cur.execute(f"INSERT INTO Score(id_user,difficulte_jeu,score_centiseconds,custom) VALUES({id_user},'{difficulty}','{score_centiseconds}','NULL')").fetchone()

class Pseudo(BaseModel):
    pseudo: str
@app.post("/profile_page/get_score")
async def get_score(request:Request,player:Pseudo=None):
    """
    Hyp: Après une demande du code java script, récupère le score de l'utilisateur et le donne à java script
    """
    if player is None:
        player=request.cookies.get("username")
    else:
        player=player.pseudo
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        score_facile = cur.execute(f"SELECT Score.score_centiseconds FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{player}' and Score.difficulte_jeu=='facile' ORDER BY Score.date_jeu ASC").fetchall()
        score_moyen = cur.execute(f"SELECT Score.score_centiseconds FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{player}' and Score.difficulte_jeu=='moyen' ORDER BY Score.date_jeu ASC").fetchall()
        score_difficile = cur.execute(f"SELECT Score.score_centiseconds FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{player}' and Score.difficulte_jeu=='difficile' ORDER BY Score.date_jeu ASC").fetchall()
    facile = [score[0]//100 for score in score_facile]
    moyen = [score[0]//100 for score in score_moyen]
    difficile = [score[0]//100 for score in score_difficile]
    return JSONResponse(content=[facile,moyen,difficile,player])


class Matrice(BaseModel):
    matrice: list[str]
    taille: int

@app.post("/custom_create/data",response_class=HTMLResponse)
async def data(matrice:Matrice,request:Request):
    """
    Hyp: Après une demande du code java script, enrengistre le champ (fourni par js) crée par l'utilisateur dans la bdd
    """
    username=request.cookies.get("username")
    champ=[]
    index=0
    for i in range(matrice.taille):
        ligne=[]
        for k in range(matrice.taille):
            if matrice.matrice[index]=='cell':
                ligne.append(0)
            else:
                ligne.append(9)
            index+=1
        champ.append(ligne)
    positions_mine = [(row, col) for row, line in enumerate(champ) for col, value in enumerate(line) if value == 9] #Cherche la position des mines (x,y)
    plateau=init_compte(champ,positions_mine)
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        id_user=cur.execute(f"SELECT id_user FROM Joueur WHERE user_pseudo=='{username}'").fetchone()[0]
        cur.execute(f"INSERT INTO Champ(user_id,difficulte,champ) VALUES({id_user},'{matrice.taille}*{matrice.taille}','{plateau}')").fetchone()

class get_mine(BaseModel):
    id_champ: int

@app.post("/custom_create/get_mine")
async def get_mine(matrice: get_mine):
    """
    Hyp: Après une demande de js, envoie le champ de mine au code java script avec l'id champ aussi fourni par java script
    """
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        champ=cur.execute(f"SELECT champ FROM Champ WHERE id_champ=='{matrice.id_champ}'").fetchone()[0]
    return JSONResponse(content=champ)

@app.post("/custom_create/done")
async def done():
    """
    Hyp: Permet simplement de rediriger l'utilisateur vers /custom_create/play lors qu'il a fini de crée son champ de mine
    """
    return RedirectResponse(url="/custom_create/play",status_code=303)

@app.get("/custom_create/play")
def play(request:Request):
    """
    Hyp: Permet de jouer au champ de mine custom crée par les utilisateurs avec un simple id_champ (fourni à la création du champ)
    """
    username=request.cookies.get("username")
    if username is None:
        id_champ=""
        return templates.TemplateResponse(
            'custom_play.html',
            {
                'request':request,
                "id_champ": id_champ,
            }
        )
    mdp= request.cookies.get("password")
    if verif_mdp(username,mdp) is False: ## Vérifie si quelqu'un à modifier le cookie username pour usurper l'identité de quelqu'un d'autre.
        return templates.TemplateResponse(
                    "error.html", 
                    {"request": request, "message":"ERREUR GRAVE: Le nom d'utilisateur et le mot de passe ne correspond pas à la base de données!"})
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        id_user=cur.execute(f"SELECT id_user FROM Joueur WHERE user_pseudo=='{username}'").fetchone()[0]
        id_champ = cur.execute(f"SELECT id_champ FROM Champ WHERE user_id=={id_user} ORDER BY id_champ DESC LIMIT 1").fetchone()
    if id_champ is None:
        id_champ = ""
    else:
        id_champ=id_champ[0]
    return templates.TemplateResponse(
            'custom_play.html',
            {
                'request':request,
                "id_champ": id_champ,
            }
    )

from init_champ import init_compte, init_plateau_mine, liste_voisins
from creation_plateau_demineur import plateau_jeu_possible_facil

@app.get("/demineur/get_mine")
async def get_mine(request:Request)->str:
    """
    Hyp: Fourni une matrice (champ de mine) à java script pour qu'il puisse l'affiche à l'utilisateur
    """
    difficulty = request.cookies.get("difficulty")
    if difficulty=="facile":
        nb_mines = 5*5*0.2
        taille = 5
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        #plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U)) 
        plateau_jeu = str(plateau_jeu_possible_facil(taille,nb_mines,[0,0]))
    elif difficulty=="moyen":
        nb_mines = 10*10*0.25
        taille = 10
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U)) 
        #plateau_jeu = str(plateau_jeu_possible(taille,nb_mines,[0,0]))
    elif difficulty=="difficile":
        nb_mines = 15*15*0.30
        taille = 15
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U))
        #plateau_jeu = str(plateau_jeu_possible(taille,nb_mines,[0,0]))
    else:
        return "Erreur"
    return plateau_jeu

import random
import asyncio
# Fonction pour simuler les données du joystick
async def simuler_joystick(websocket: WebSocket):
    position = [0, 0]
    while True:
        # Générer des valeurs aléatoires pour le joystick
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)

        # Mettre à jour la position simulée
        position[0] = (position[0] + x // 50) % 10  # Valeurs entre 0 et 9
        position[1] = (position[1] + y // 50) % 10  # Valeurs entre 0 et 9

        # Envoyer les données au client via WebSocket
        await websocket.send_json({
            "position": position
        })

        await asyncio.sleep(0.5)  # Pause de 500 ms entre les mises à jour

# Fonction pour simuler les appuis sur un bouton
async def simuler_bouton(websocket: WebSocket):
    while True:
        # Attendre un temps aléatoire avant de simuler un appui
        await asyncio.sleep(random.randint(2, 5))  # Pause de 2 à 5 secondes

        # Envoyer un événement "button_pressed" au client
        await websocket.send_json({
            "event": "button_pressed"
        })

# Endpoint WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Simule les interactions joystick et bouton pour tester la communication WebSocket.
    """
    await websocket.accept()
    try:
        # Lancer simultanément les simulations du joystick et du bouton
        await asyncio.gather(
            simuler_joystick(websocket),
            simuler_bouton(websocket)
        )
    except WebSocketDisconnect:
        print("Client déconnecté.")
    except Exception as e:
        print("Erreur dans l'endpoint WebSocket :", e)
    finally:
        print("Connexion WebSocket fermée.")

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug<
