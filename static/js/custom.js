const slider = document.getElementById("range_t");
const output = document.getElementById("demo");
demineur("5")
output.innerHTML = "5x5";
slider.oninput = () => {
    const size = parseInt(slider.value); // Get slider value
    demineur(size); // Call demineur with variables
};
function demineur(size) {
    nb_mine_autoriser = Math.round(size*size*0.2)
    nb_mine = 0
    nb_mine_affichage = document.getElementById("nb_mine")
    update_mine()

    output.innerHTML = size+'x'+size;
    const gameContainer = document.getElementById("game-container");
    gameContainer.innerHTML=''
    async function initBoard(rows, cols) {
        gameContainer.style.gridTemplateRows = `repeat(${rows},40px)`;
        gameContainer.style.gridTemplateColumns = `repeat(${cols},40px)`;

        // Generate cells
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.addEventListener("click", () => placeBombe(row, col));
    
            // Clic droit pour ajouter/enlever un drapeau
            cell.addEventListener("contextmenu", (e) => {
              e.preventDefault();
              placeBombe(row, col);
            });
            gameContainer.appendChild(cell);
            }
        }
    }
    initBoard(size, size);

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