window.onload = function() {
  const ham_button = document.querySelector('.hamburger');
  const get = document.querySelector(".navbar");

  ham_button.addEventListener('click', function (){
    ham_button.classList.toggle('is-active');
    get.classList.toggle('is-active');
  });
};

async function get_mine() {
  const url = 'http://127.0.0.1:8000/demineur/get_mine'; // L'URL de ton endpoint
  const response = await fetch(url); // Requête GET simple
  const result = await response.json(); // Parse le résultat JSON
  return JSON.parse(result);
}

//Création d'une fonction pour éviter de simplement envoyer le champ de mine sur html qui est visible par tous
//Alors que la version précédent, on pouvait juste F12 et voir les réponses, maintenant les réponses ne sont plus visibles.

async function init(){ 
//Initialisation des Constantes
const solutionMatrix = await get_mine()
const gameContainer = document.getElementById("game-container");
const rows = solutionMatrix.length;
const cols = solutionMatrix[0].length;
//Fin

//Initialisation des variables
temps = document.getElementById("timer")
let interval = 0
chrono=0
compteur=false
game=true
nb_uncovered=0
nb_mine=solutionMatrix.flat().filter(value => value === 9).length; // Compte le nombre de mines dans la grille

// Fin
    
gameContainer.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
gameContainer.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    
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

    // Fonction pour révéler une case
async function revealCell(row, col) {
  if (compteur===false){
    interval = setInterval(update_Timer,10)
    compteur=true
  }
  if (game===false){
    return
  }
  const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
  if (cell.classList.contains("revealed")){
    revealNeighborsIfFlagsMatch(row,col);
    return
  }

  const value = solutionMatrix[row][col];

  if (value === 9) {
    clearInterval(interval)
    cell.classList.add("mine");
    cell.textContent = "💣";
    game=false
    temps = document.getElementById("timer")
    alert("Vous avez perdu! Votre temps est "+ temps.textContent)
  } else if (value === 0) {
    revealAdjacentCells(row,col)
  } else {
    nb_uncovered++
    cell.classList.add("revealed");
    cell.textContent = value;
  }
  check_win()
}

function revealAdjacentCells(row, col) {
  const directions = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1],           [0, 1],
    [1, -1], [1, 0], [1, 1],
  ];
  const stack = [[row, col]]; // Utilisation d'une pile

  while (stack.length > 0) {
    const [currentRow, currentCol] = stack.pop();
    const currentCell = document.querySelector(`[data-row="${currentRow}"][data-col="${currentCol}"]`);
    if (!currentCell || currentCell.classList.contains("revealed")) continue; 
    currentCell.classList.add("revealed");
    const value = solutionMatrix[currentRow][currentCol];
    nb_uncovered++;
    if (value === 0) {
      directions.forEach(([dRow, dCol]) => {
        const newRow = currentRow + dRow;
        const newCol = currentCol + dCol;
        if (
          //solutionMatrix[newRow,newCol]===0
          newRow >= 0 &&  
          newRow < solutionMatrix.length &&
          newCol >= 0 &&
          newCol < solutionMatrix[0].length
        ) {
          stack.push([newRow, newCol]);
        }
      });
    } else {
      currentCell.textContent = value;
    }
  }
}
    
// Fonction pour ajouter un drapeau
function toggleFlag(row, col) {
  if (game===false){
    return
  }
  const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
  if (cell.classList.contains("revealed")) return;
  cell.classList.toggle("flagged");
  cell.textContent = cell.classList.contains("flagged") ? "🚩" : "";
  check_win()
}
async function check_win(){
  if (nb_uncovered === ((rows * cols) - nb_mine)) {
    clearInterval(interval)
    game=false
    temps=document.getElementById("timer")
    send_score(temps.textContent)
    alert("Vous avez gagné ! Félicitations ! Votre temps est de "+temps.textContent);
  }
}

async function send_score(scoreStr){
  //const [minutes, seconds, centiseconds] = scoreStr.split(/[:.]/).map(Number);
  //const totalCentiseconds = (minutes * 60 * 100) + (seconds * 100) + centiseconds;
  //console.log(chrono-1)
  //console.log(totalCentiseconds)

  const url = 'http://127.0.0.1:8000/demineur/score'
  fetch(url,{
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ score: chrono-1}),
  })
}

// Timer
function update_Timer(){
  const minutes= Math.floor(chrono/100/60);
  centisecondes = chrono%100
  secondes = Math.floor(chrono/100) %60
  centisecondes=centisecondes<10 ? '0' + centisecondes : centisecondes;
  secondes=secondes<10 ? '0' + secondes : secondes;
  temps.innerHTML=`${minutes}:${secondes}.${centisecondes}`;
  chrono++;
}

  // Ajout de la fonction pour vérifier et révéler les voisins si le nombre de drapeaux correspond au numéro de la cellule
function revealNeighborsIfFlagsMatch(row, col) {
  if (!game) return; // Si le jeu est terminé, ne rien faire

  const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
  const value = parseInt(cell.textContent, 10); // Récupère la valeur de la cellule
  if (isNaN(value) || value === 0) return; // Ignore si la cellule ne contient pas de nombre

  const directions = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1],           [0, 1],
    [1, -1], [1, 0], [1, 1],
  ];

  let flagCount = 0;

  directions.forEach(([dRow, dCol]) => {
    const newRow = row + dRow;
    const newCol = col + dCol;
    const neighbor = document.querySelector(`[data-row="${newRow}"][data-col="${newCol}"]`);

    if (neighbor && neighbor.classList.contains("flagged")) {
      flagCount++;
    }
  });

  // Si le nombre de drapeaux correspond à la valeur de la cellule
  if (flagCount === value) {
    directions.forEach(([dRow, dCol]) => {
      const newRow = row + dRow;
      const newCol = col + dCol;
      const neighbor = document.querySelector(`[data-row="${newRow}"][data-col="${newCol}"]`);

      if (neighbor && !neighbor.classList.contains("revealed") && !neighbor.classList.contains("flagged")) {
        revealCell(newRow, newCol);
      }
    });
  }
}


}

init() //Initialisation du démineur
var x, i, j, l, ll, selElmnt, a, b, c;
/*look for any elements with the class "custom-select":*/
x = document.getElementsByClassName("custom-select");
l = x.length;
for (i = 0; i < l; i++) {
  selElmnt = x[i].getElementsByTagName("select")[0];
  ll = selElmnt.length;
  /*for each element, create a new DIV that will act as the selected item:*/
  a = document.createElement("DIV");
  a.setAttribute("class", "select-selected");
  a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
  x[i].appendChild(a);
  /*for each element, create a new DIV that will contain the option list:*/
  b = document.createElement("DIV");
  b.setAttribute("class", "select-items select-hide");
  for (j = 1; j < ll; j++) {
    /*for each option in the original select element,
    create a new DIV that will act as an option item:*/
    c = document.createElement("DIV");
    c.innerHTML = selElmnt.options[j].innerHTML;
    c.setAttribute("data-value", selElmnt.options[j].value); // Store the value in a data attribute
    c.addEventListener("click", function(e) {
        /*when an item is clicked, update the original select box,
        and the selected item:*/
        var y, i, k, s, h, sl, yl;
        s = this.parentNode.parentNode.getElementsByTagName("select")[0];
        sl = s.length;
        h = this.parentNode.previousSibling;
        for (i = 0; i < sl; i++) {
          if (s.options[i].innerHTML == this.innerHTML) {
            s.selectedIndex = i;
            h.innerHTML = this.innerHTML;
            y = this.parentNode.getElementsByClassName("same-as-selected");
            yl = y.length;
            for (k = 0; k < yl; k++) {
              y[k].removeAttribute("class");
            }
            this.setAttribute("class", "same-as-selected");
            break;
          }
        }
        // Perform redirection based on the selected value
        const selectedValue = s.options[s.selectedIndex].value;
        if (selectedValue) {
          window.location.href = selectedValue; // Redirect to the URL
        }
        h.click();
    });
    b.appendChild(c);
  }
  x[i].appendChild(b);
  a.addEventListener("click", function(e) {
      /*when the select box is clicked, close any other select boxes,
      and open/close the current select box:*/
      e.stopPropagation();
      closeAllSelect(this);
      this.nextSibling.classList.toggle("select-hide");
      this.classList.toggle("select-arrow-active");
    });
}
function closeAllSelect(elmnt) {
  /*a function that will close all select boxes in the document,
  except the current select box:*/
  var x, y, i, xl, yl, arrNo = [];
  x = document.getElementsByClassName("select-items");
  y = document.getElementsByClassName("select-selected");
  xl = x.length;
  yl = y.length;
  for (i = 0; i < yl; i++) {
    if (elmnt == y[i]) {
      arrNo.push(i)
    } else {
      y[i].classList.remove("select-arrow-active");
    }
  }
  for (i = 0; i < xl; i++) {
    if (arrNo.indexOf(i)) {
      x[i].classList.add("select-hide");
    }
  }
}
/*if the user clicks anywhere outside the select box,
then close all select boxes:*/
document.addEventListener("click", closeAllSelect);

// Connexion au WebSocket
const socket = new WebSocket("ws:///127.0.0.1:8000/ws");

// Fonction appelée pour utiliser les données du joystick
function utiliserDonneesJoystick(x, y) {
    console.log("Données du joystick :", { x, y });
    // Ajoute ici la logique avec x et y
}

// Lorsqu'un message est reçu depuis le WebSocket
socket.onmessage = function(event) {
    const data = JSON.parse(event.data); // Parse les données JSON
    const x = data.x;
    const y = data.y;

    // Exécute la fonction avec les coordonnées
    utiliserDonneesJoystick(x, y);
};

// Gestion des erreurs
socket.onerror = function(error) {
    console.error("Erreur WebSocket :", error);
};

// Lorsqu'une connexion est établie
socket.onopen = function() {
    console.log("Connexion WebSocket ouverte.");
};

// Lorsqu'une connexion est fermée
socket.onclose = function() {
    console.log("Connexion WebSocket fermée.");
};