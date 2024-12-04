import uvicorn
from fastapi import Form
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


def require_login():
    # Replace with real authentication logic
    authenticated = False  # Simulating that the user is not authenticated
    if not authenticated:
        return RedirectResponse(url="/login")
    return True

@app.get("/")
async def home():
    return RedirectResponse(url="/login")

@app.get("/protected", dependencies=[Depends(require_login)])
async def protected():
    return {"message": "This is a protected route."}

@app.get("/jeu")

@app.post("/soumettre", response_class=HTMLResponse)
async def submit_form(request: Request, username: str = Form(...), password: str = Form(...)):
    # Process the data here if needed (e.g., save to database, validate, etc.)
    # Render a new page displaying the submitted data
    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        data = cur.execute("SELECT * FROM Joueur").fetchone()

    return templates.TemplateResponse(
        "jeu.html", 
        {"request": request, "data":data, "username": username, "password": password , 'hashed_username': sha256(username.encode('utf-8')).hexdigest(),'hashed_password': sha256(password.encode('utf-8')).hexdigest()}
    )

@app.get("/login")
async def login(request:Request):
    return templates.TemplateResponse('login.html',{'request': request,'title':'Login page',})

@app.get("/inscription")
def inscription(request:Request):
    return templates.TemplateResponse('inscription.html',{'request': request,'title':'Inscription page',})

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug