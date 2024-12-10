function validateForm() { /* pas nécéssaire pour le moment*/
    let isValid = true;

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");

    usernameError.textContent = "";
    passwordError.textContent = "";

    if (!username) {
        usernameError.textContent = "Pseudo ne peut pas être vide";
        isValid = false;
    }

    if (!password) {
        passwordError.textContent = "Mot de passe ne peut pas être vide";
        isValid = false;
    }

    return isValid;
}

// script.js

// Exemple de matrice générée par Python
//const solutionMatrix = [
//    ["1", "9", "2"],
//    ["2", "3", "9"],
//    ["9", "3", "1"],
//  ];

  const element = document.getElementById('test');
  const solutionMatrix = JSON.parse(element.textContent);
  // Génère la grille dans le conteneur
  const gameContainer = document.getElementById("game-container");
  const rows = solutionMatrix.length;
  const cols = solutionMatrix[0].length;
  
  gameContainer.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
  gameContainer.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
  
  // Fonction pour révéler une case
  function revealCell(row, col) {
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains("revealed")) return;
  
    cell.classList.add("revealed");
    const value = solutionMatrix[row][col];
  
    if (value === 9) {
      cell.classList.add("mine");
      cell.textContent = "💣";
      alert("Game Over!");
    } else {
      cell.textContent = value;
    }
  }
  
  // Fonction pour ajouter un drapeau
  function toggleFlag(row, col) {
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains("revealed")) return;
  
    cell.classList.toggle("flagged");
    cell.textContent = cell.classList.contains("flagged") ? "🚩" : "";
  }
  
  // Génération des cellules
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = row;
      cell.dataset.col = col;
  
      // Clic gauche pour révéler
      cell.addEventListener("click", () => revealCell(row, col));
  
      // Clic droit pour ajouter/enlever un drapeau
      cell.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        toggleFlag(row, col);
      });
  
      gameContainer.appendChild(cell);
    }
  }
  

  async function callPythonFunction() {
    const url = 'http://127.0.0.1:8000/simple_function'; // L'URL de ton endpoint

    try {
        const response = await fetch(url); // Requête GET simple
        const result = await response.json(); // Parse le résultat JSON
        console.log(result); // Affiche {"result": "Hello, World!"}
    } catch (error) {
        console.error("Erreur :", error);
    }
}