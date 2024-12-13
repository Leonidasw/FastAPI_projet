window.onload = function() {
    // Récupère l'URL actuelle
    const urlParams = new URLSearchParams(window.location.search);

    // Récupère la valeur de "id_champ"
    const idChamp = urlParams.get('id_champ');
    if (idChamp !== null){
        console.log(idChamp);
        get_mine(idChamp)
    }
}


function get_mine(idChamp){
    const url = 'http://127.0.0.1:8000/custom_create/get_mine'
    fetch(url,{
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id_champ : idChamp}),
    })
    .then(response => response.json())
    .then(data => {init(JSON.parse(data))});
}

async function init(champ){ 
  //Initialisation des Constantes
  const solutionMatrix = champ
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
      console.log(interval)
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
      alert("Vous avez gagné ! Félicitations ! Votre temps est de "+temps.textContent);
        }
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
  }}