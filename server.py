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
async def demineur(request:Request):
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

@app.get('/custom_create')
async def create_board(request:Request):
    username = request.cookies.get("username")
    if username is None:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        "custom_create.html", 
        {"request": request})  
@app.get('/custom_create_william')
async def create_board(request:Request):
    username = request.cookies.get("username")
    if username is None:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        "custom_create_william.html", 
        {"request": request})      


from init_champ import init_compte, init_plateau_mine, liste_voisins

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
    print("SCORE ENVOYER DANS LA BDD")

class Matrice(BaseModel):
    matrice: list[str]
    taille: int

@app.post("/custom_create/data",response_class=HTMLResponse)
async def data(matrice:Matrice,request:Request):
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
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        champ=cur.execute(f"SELECT champ FROM Champ WHERE id_champ=='{matrice.id_champ}'").fetchone()[0]
    return JSONResponse(content=champ)

@app.post("/custom_create/done")
async def done():
    return RedirectResponse(url="/custom_create/play",status_code=303)

@app.get("/custom_create/play")
def play(request:Request):
    with sqlite3.connect(dbpath) as connection:
        cur = connection.cursor()
        id_champ = cur.execute("SELECT id_champ FROM Champ ORDER BY id_champ DESC LIMIT 1").fetchone()
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

@app.get("/demineur/get_mine")
async def get_mine(request:Request):
    difficulty = request.cookies.get("difficulty")
    if difficulty=="facile":
        nb_mines = 5
        taille = 5
        case_joueur=(0,0)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U))
    elif difficulty=="moyen":
        nb_mines = 15
        taille = 10
        case_joueur=(1,1)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U)) 
    elif difficulty=="difficile":
        nb_mines = 30
        taille = 15
        case_joueur=(1,1)
        case_U= liste_voisins(case_joueur, taille)+[case_joueur]
        plateau_jeu = str(init_plateau_mine(taille, nb_mines,case_U))
    else:
        return "Erreur"
    return plateau_jeu

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug