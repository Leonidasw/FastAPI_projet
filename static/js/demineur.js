async function get_mine() {
    const url = 'http://127.0.0.1:8000/demineur/get_mine'; // L'URL de ton endpoint
    const response = await fetch(url); // Requête GET simple
    const result = await response.json(); // Parse le résultat JSON
    return JSON.parse(result);
  }

async function timer() {
  const url = 'http://127.0.0.1:8000/timer';
  const response = await fetch(url);
  const result = await response.json();
  return result
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
  compteur=false
  game=true
  nb_de_flag=0
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
      timer()
      compteur=true
    }
    if (game===false){
      return
    }
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains("revealed")) return;

    cell.classList.add("revealed");
    const value = solutionMatrix[row][col];

    if (value === 9) {
      cell.classList.add("mine");
      cell.textContent = "💣";
      game=false
      const temps = await timer()
      alert("Vous avez perdu! Votre temps est "+temps)
    } else {
      cell.textContent = value;
    }
  nb_uncovered++
  check_win()
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
    nb_de_flag++
    check_win()
  }
  async function check_win(){
    if (nb_de_flag === nb_mine && nb_uncovered === (rows * cols - nb_mine)) {
      game=false
      const temps = await timer()
      alert("Vous avez gagné ! Félicitations ! Votre temps est de "+temps);
    }
  }


}

init()