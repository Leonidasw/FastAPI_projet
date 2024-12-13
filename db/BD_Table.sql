CREATE TABLE IF NOT EXISTS Joueur (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,   -- Clé primaire auto-incrémentée
    user_pseudo TEXT UNIQUE NOT NULL,            -- Pseudo unique
    user_mdp TEXT NOT NULL,                      -- Mot de passe crypté
    data_creation DATE DEFAULT CURRENT_TIMESTAMP -- Date de création, valeur par défaut = date actuelle
);

CREATE TABLE IF NOT EXISTS Score (
    id_score INTEGER PRIMARY KEY AUTOINCREMENT,  -- Clé primaire auto-incrémentée
    date_jeu DATETIME DEFAULT CURRENT_TIMESTAMP, -- Date de la partie jouée, par défaut = date actuelle
    id_user INTEGER,                             -- Clé étrangère référencée depuis la table Joueur
    difficulte_jeu TEXT,                         -- Difficulté du jeu
    time_jeu REAL,                               -- Temps de jeu
    custom BOOL,                                 -- Partie personnalisée
    FOREIGN KEY (id_user) REFERENCES Joueur (id_user)
);

CREATE TABLE IF NOT EXISTS Champ (
    id_champ INTEGER PRIMARY KEY AUTOINCREMENT,  -- Clé primaire auto-incrémentée
    user_id INTEGER,                             -- Clé étrangère référencée depuis la table Joueur
    difficulte TEXT,                             -- Taille du champ de mine
    champ TEXT,
    FOREIGN KEY (user_id) REFERENCES Joueur (id_user) -- Référence à la table Joueur
);

