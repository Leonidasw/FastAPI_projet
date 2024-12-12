import uvicorn
from fastapi import Form, Response
from fastapi import FastAPI, Request # import de la classe FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from hashlib import sha256
from contextlib import asynccontextmanager
import sqlite3
import os

dbpath = os.path.join(os.path.dirname(__file__), "db", "database.db")

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

def verif_mdp(username,mdp):
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        db_mdp = cur.execute(f"SELECT user_mdp FROM Joueur WHERE user_pseudo=='{username}'").fetchone()
    return mdp==db_mdp[0]

@app.post("/soumettre_login", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
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
    response = RedirectResponse(url="/login")
    response.delete_cookie("username")
    response.delete_cookie("password")
    return response

@app.get("/login")
async def login(request:Request):
    username = request.cookies.get("username")
    if username is None:
        return templates.TemplateResponse('login.html',{'request': request,'title':'Login page',})
    return RedirectResponse(url="/profile_page")
    

@app.get("/inscription")
async def inscription(request:Request):
    username = request.cookies.get("username")
    if username is not None:
        return RedirectResponse(url="/profile_page")
    return templates.TemplateResponse('inscription.html',{'request': request,'title':'Inscription page',})

@app.get("/profile_page")
async def profile_page(request:Request):
    username = request.cookies.get("username")
    if username is None:
        return RedirectResponse(url="/login")
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
    jeux=cur.execute(f"SELECT COUNT(*) FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{username}';").fetchone()[0]
    temps = cur.execute(f"SELECT MIN(Score.time_jeu) FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{username}';").fetchone()[0]
    return templates.TemplateResponse(
                "profile_page.html", 
                {"request": request, "username": username,"games":jeux,"time":temps})        

@app.post("/soumettre_register", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
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
    return RedirectResponse(url="/demineur/facile",status_code=303)
    #return templates.TemplateResponse('demineur.html',{'request': request,'title':"Démineur", 'inscrit':''})

@app.get('/leaderboard')
async def leaderboard(request:Request):
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        data = cur.execute("SELECT Joueur.user_pseudo,Score.time_jeu,Score.date_jeu,Score.difficulte_jeu FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user ORDER BY Score.time_jeu ASC").fetchall()
        wins = cur.execute("SELECT Joueur.user_pseudo, COUNT(Score.id_user) AS appearances FROM Score JOIN Joueur ON Score.id_user = Joueur.id_user GROUP BY Joueur.user_pseudo ORDER BY appearances DESC;").fetchall()
    return templates.TemplateResponse(
        'leaderboard.html',
        {
            'request': request,
            'title': "Leaderboard",
            'score': data,
            'wins':wins,
            'enumerate': enumerate  # Add `enumerate` to the template context
        }
    )

@app.get('/demineur/custom_create')
async def create_board(request:Request):
    username = request.cookies.get("username")
    if username is None:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        "custom_create.html", 
        {"request": request})    

from pydantic import BaseModel
class Score(BaseModel):
    score: str

@app.post("/demineur/score")
async def score(score: Score,request:Request):
    username=request.cookies.get("username")
    difficulty=request.cookies.get("difficulty")
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        id_user=cur.execute(f"SELECT id_user FROM Joueur WHERE user_pseudo=='{username}'").fetchone()[0]
        cur.execute(f"INSERT INTO Score(id_user,difficulte_jeu,time_jeu,custom) VALUES({id_user},'{difficulty}','{score.score}',False)").fetchone()
    return JSONResponse(content=score.score)  # Renvoie le score reçu

from init_champ import init_plateau_mine, liste_voisins

@app.get("/demineur/facile")
async def demineur_facile(request:Request):
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
    
@app.get("/demineur/get_mine")
async def get_mine(request:Request):
    difficulty = request.cookies.get("difficulty")
    if difficulty=="facile":
        taille = 5
        nb_mines = taille*taille*0.2
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U))
    elif difficulty=="moyen":
        taille = 10
        nb_mines = taille*taille*0.2
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U)) 
    elif difficulty=="difficile":
        taille = 15
        nb_mines = taille*taille*0.2
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U))
    else:
        return "Erreur"
    return plateau_jeu

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug