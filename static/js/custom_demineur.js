const jeuVide = document.getElementById("game-container");
function custom_demineur(taille){
    nb_mine_autoriser = taille*taille*0.2
    nb_mine = 0
    nb_mine_affichage = document.getElementById("nb_mine")
    update_mine()
    while (jeuVide.firstChild){ //Supprimer ce qu'il y a dans le champ de mine précedent
        jeuVide.removeChild(jeuVide.firstChild)
    }
    const gameContainer = jeuVide;
    gameContainer.style.gridTemplateRows = `repeat(${taille}, 1fr)`;
    gameContainer.style.gridTemplateColumns = `repeat(${taille}, 1fr)`;
    const rows = taille
    const cols= taille
    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          const cell = document.createElement("div");
          cell.classList.add("cell");
          cell.dataset.row = row;
          cell.dataset.col = col;
    
          // Clic gauche pour révéler
          cell.addEventListener("click", () => placeBombe(row, col));
    
          // Clic droit pour ajouter/enlever un drapeau
          cell.addEventListener("contextmenu", (e) => {
            e.preventDefault();
            placeBombe(row, col);
          });
    
          gameContainer.appendChild(cell);
        }
    }

    function placeBombe(row,col){
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        if (cell.className==="cell mine"){
            cell.classList.replace("mine","cell")
            cell.textContent = ""
            nb_mine--
            update_mine()
            return
        }
        if (nb_mine_autoriser-nb_mine!==0){
            cell.classList.add("mine");
            cell.textContent = "💣";
            nb_mine++
            update_mine()
        }
    }

    function update_mine(){
        affichage=nb_mine_autoriser-nb_mine
        nb_mine_affichage.innerHTML=`Nombre de mine: ${affichage}`
    }
}

function publier(){
    alert("ne fait rien pour l'instant")
}