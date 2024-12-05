import uvicorn
from fastapi import Form, Response
from fastapi import FastAPI, Request # import de la classe FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from hashlib import sha256
from contextlib import asynccontextmanager
import sqlite3


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ouvrir la connexion SQLite au démarrage de l'application
    connection = sqlite3.connect("database.db")
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


"""def require_login():
    # Replace with real authentication logic
    authenticated = False  # Simulating that the user is not authenticated
    if not authenticated:
        return RedirectResponse(url="/login")
    return True"""

@app.get("/")
async def home():
    return RedirectResponse(url="/login")

"""@app.get("/protected", dependencies=[Depends(require_login)])
async def protected():
    return {"message": "This is a protected route."}"""

"""@app.get("/jeu")
"""

def verif_mdp(username,mdp):
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        db_mdp = cur.execute(f"SELECT user_mdp FROM Joueur WHERE user_pseudo=='{username}'").fetchone()
    return mdp==db_mdp[0]

@app.post("/soumettre_login", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        data = cur.execute(f"SELECT * FROM Joueur WHERE user_pseudo=='{username}'").fetchone()
    ### Vérification du mot de passe ####
    if data is None:
        return templates.TemplateResponse('login.html',{'request': request,'Valide':"Le nom d'utilisateur n'existe pas!"}) 
    mdp= sha256(password.encode('utf-8')).hexdigest()
    jeux=cur.execute(f"SELECT COUNT(*) FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{username}';").fetchone()[0]
    if verif_mdp(username,mdp):
        response = templates.TemplateResponse(
            "profile_page.html", 
            {"request": request, "username": username, "password": password, 
            'hashed_password': sha256(password.encode('utf-8')).hexdigest(),
            'data':data,'games':jeux}
        )
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
    return templates.TemplateResponse('inscription.html',{'request': request,'title':'Inscription page',})

@app.get("/profile_page")
async def profile_page(request:Request):
    username = request.cookies.get("username")
    if username is None:
        return RedirectResponse(url="/login")
    password = request.cookies.get("password") 
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        data = cur.execute(f"SELECT * FROM Joueur WHERE user_pseudo=='{username}'").fetchone()   
    return templates.TemplateResponse(
                "profile_page.html", 
                {"request": request, "username": username, "password": password, 
                'hashed_password': sha256(password.encode('utf-8')).hexdigest(),
                'data':data})        

@app.post("/soumettre_register", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        test_user = cur.execute(f"SELECT * FROM Joueur WHERE user_pseudo=='{username}'   ").fetchone()
        password=sha256(password.encode('utf-8')).hexdigest()
        if test_user is None:
            cur.execute(f"INSERT INTO Joueur(user_pseudo, user_mdp) VALUES('{username}','{password}')").fetchone()
            data = cur.execute(f"SELECT * FROM Joueur WHERE user_pseudo=='{username}'").fetchone()
            jeux=cur.execute(f"SELECT COUNT(*) FROM Score JOIN Joueur ON Score.id_user=Joueur.id_user WHERE Joueur.user_pseudo=='{username}';").fetchone()[0]
            response = templates.TemplateResponse(
                "profile_page.html", 
                {"request": request, "username": username, "password": password, 
                'hashed_password': sha256(password.encode('utf-8')).hexdigest(),
                'data':data , 'games':jeux}
            )
            response.set_cookie(key="username", value=username)
            response.set_cookie(key="password", value=password)
            return response
        return templates.TemplateResponse('inscription.html',{'request': request,'Valide':"Le nom d'utilisateur est déjà utilisé"})
    
@app.get("/demineur")
async def demineur(request:Request):
    return templates.TemplateResponse('demineur.html',{'request': request,'title':"Démineur"})

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug