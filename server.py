import uvicorn
from fastapi import Form
from fastapi import FastAPI, Request # import de la classe FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from hashlib import sha256

templates = Jinja2Templates(directory="templates/")
app = FastAPI() # Création de l application

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
    return templates.TemplateResponse(
        "jeu.html", 
        {"request": request, "username": username, "password": password , 'hashed_username': sha256(username.encode('utf-8')).hexdigest(),'hashed_password': sha256(password.encode('utf-8')).hexdigest()}
    )

@app.get("/login")
async def login(request:Request):
    return templates.TemplateResponse('login.html',{'request': request,'title':'Login page',})

@app.get("/inscription")
def inscription(request:Request):
    return templates.TemplateResponse('inscription.html',{'request': request,'title':'Inscription page',})

if __name__ == "__main__":
    uvicorn.run(app) # lancement du serveur HTTP + WSGI avec les options de debug