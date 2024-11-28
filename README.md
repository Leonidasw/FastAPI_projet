Project Overview
This project is a FastAPI-based web application with a structured directory layout for organizing server code, templates, and static files like CSS and JavaScript.

File Structure
plaintext
Copy code
project/
├── serveur.py              # The main Python file that runs the FastAPI server
├── templates/
│   ├── login.html          # Login page template (Jinja2 format)
│   ├── jeu.html            # Game page template
│   └── inscription.html    # Registration page template
├── static/
│   ├── css/
│   │   └── style.css       # Styling for the application
│   └── js/
│       └── script.js       # JavaScript for client-side interactivity
