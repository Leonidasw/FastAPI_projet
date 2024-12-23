
const canvas = document.getElementById("demineurCanvas");
const ctx = canvas.getContext("2d");

// Taille des cases
const cellSize = 30;

// Couleurs
const colors = {
    empty: "#d3d3d3",
    flagged: "#e74c3c",
    mine: "#2c3e50",
    border: "#000000",
    flagPole: "#8b4513",
    flag: "#e74c3c",
    covered:"#979fad"
};

// Fonction pour dessiner une cellule vide avec style
function drawCell(x, y, fillColor) {
    ctx.fillStyle = fillColor;
    ctx.fillRect(x, y, cellSize, cellSize);

    // Ajouter une bordure
    ctx.strokeStyle = colors.border;
    ctx.strokeRect(x, y, cellSize, cellSize);
}

function drawCovered(x, y, fillColor) {
    ctx.fillStyle = fillColor;
    ctx.fillRect(x, y, cellSize, cellSize);

    ctx.fillStyle = colors.covered;
    ctx.beginPath();
    ctx.arc(x + cellSize / 2, y + cellSize / 2, cellSize / 5, 0, 2 * Math.PI);
    ctx.fill();

    // Ajouter une bordure
    ctx.strokeStyle = colors.border;
    ctx.strokeRect(x, y, cellSize, cellSize);
}


// Fonction pour dessiner une mine avec des "pics"
function drawMine(x, y) {
    drawCell(x, y, colors.empty);

    // Dessiner le cercle principal
    ctx.fillStyle = colors.mine;
    ctx.beginPath();
    ctx.arc(x + cellSize / 2, y + cellSize / 2, cellSize / 4, 0, 2 * Math.PI);
    ctx.fill();

    // Dessiner les "pics"
    ctx.strokeStyle = colors.mine;
    for (let angle = 0; angle < 360; angle += 45) {
        const rad = (angle * Math.PI) / 180;
        const startX = x + cellSize / 2 + Math.cos(rad) * (cellSize / 4);
        const startY = y + cellSize / 2 + Math.sin(rad) * (cellSize / 4);
        const endX = x + cellSize / 2 + Math.cos(rad) * (cellSize / 3);
        const endY = y + cellSize / 2 + Math.sin(rad) * (cellSize / 3);
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
    }
}

// Fonction pour dessiner un drapeau
function drawFlag(x, y) {
    drawCell(x, y, colors.empty);

    // Dessiner le mât
    ctx.fillStyle = colors.flagPole;
    ctx.fillRect(x + cellSize / 3, y + cellSize / 5, cellSize / 10, cellSize / 1.5);

    // Dessiner le drapeau
    ctx.fillStyle = colors.flag;
    ctx.beginPath();
    ctx.moveTo(x + cellSize / 3 + 2, y + cellSize / 5);
    ctx.lineTo(x + cellSize / 3 + 2, y + cellSize / 2);
    ctx.lineTo(x + cellSize / 1.3, y + cellSize / 3.1);
    ctx.closePath();
    ctx.fill();
}

// Fonction pour dessiner le tableau
function drawDemineurBoard() {
    // Première ligne : case grise et drapeau
    drawCovered(0, 0, colors.empty);
    drawFlag(cellSize, 0);

    // Deuxième ligne : mine et case grise
    drawMine(0, cellSize);
    drawCovered(cellSize, cellSize, colors.empty);
}

// Appeler la fonction pour dessiner le tableau
drawDemineurBoard();

const lb_canvas = document.getElementById("leaderboardCanvas");
const lb_ctx = lb_canvas.getContext("2d");

// Taille des cases
const lb_cellSize = 30;
function drawRect(x, y, fillColor, text, height) {
    lb_ctx.fillStyle = fillColor;
    lb_ctx.fillRect(x, y, lb_cellSize-10, height);

    // Ajouter une bordure
    lb_ctx.strokeRect(x, y, lb_cellSize-10, height);       // Font size and family

    const centerX = x + (lb_cellSize-10) / 2;
    const centerY = y + height / 2;

    lb_ctx.fillStyle = "white";       // Text color
    lb_ctx.textAlign = "center";      // Align text to the center
    lb_ctx.textBaseline = "middle"; 
    lb_ctx.strokeText(text, centerX, centerY);
    lb_ctx.fillText(text, centerX, centerY);
}
function leaderboard() {
    drawRect(15, 40, '#243191','3',-lb_cellSize/2);
    drawRect(lb_cellSize+10, 40, '#243191','1',-lb_cellSize*1.5);
    drawRect(lb_cellSize*2+5, 40, '#243191','2',-lb_cellSize+4);
}
leaderboard();

const ctm_canvas = document.getElementById("customCanvas");
const ctm_ctx = ctm_canvas.getContext("2d");

// Taille des cases
const ctm_cellSize = 20;

// Fonction pour dessiner une cellule vide avec style
function ctm_drawCovered(x, y, fillColor) {
    ctm_ctx.fillStyle = fillColor;
    ctm_ctx.fillRect(x, y, ctm_cellSize, ctm_cellSize);

    ctm_ctx.fillStyle = colors.covered;
    ctm_ctx.beginPath();
    ctm_ctx.arc(x + ctm_cellSize / 2, y + ctm_cellSize / 2, ctm_cellSize / 5, 0, 2 * Math.PI);
    ctm_ctx.fill();

    // Ajouter une bordure
    ctm_ctx.strokeStyle = colors.border;
    ctm_ctx.strokeRect(x, y, ctm_cellSize, ctm_cellSize);
}

function drawCustomBoard() {
    // Première ligne 
    ctm_drawCovered(0, 0, colors.empty);
    ctm_drawCovered(ctm_cellSize, 0, colors.empty);
    ctm_drawCovered(ctm_cellSize*2, 0, colors.empty);

    // Deuxième ligne 
    ctm_drawCovered(0, ctm_cellSize, colors.empty);
    ctm_drawCovered(ctm_cellSize,ctm_cellSize, colors.empty);
    ctm_drawCovered(ctm_cellSize*2, ctm_cellSize, colors.empty);

    ctm_drawCovered(0, ctm_cellSize*2, colors.empty);
    ctm_drawCovered(ctm_cellSize,ctm_cellSize*2, colors.empty);
    ctm_drawCovered(ctm_cellSize*2, ctm_cellSize*2, colors.empty);
}

drawCustomBoard()

Highcharts.chart('container', {

    title: {
      text: 'Solar Employment Growth by Sector, 2010-2016'
    },
  
    subtitle: {
      text: 'Source: thesolarfoundation.com'
    },
  
    yAxis: {
      title: {
        text: 'Number of Employees'
      }
    },
  
    xAxis: {
      accessibility: {
        rangeDescription: 'Range: 2010 to 2017'
      }
    },
  
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle'
    },
  
    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        },
        pointStart: 2010
      }
    },
  
    series: [{
      name: 'Installation',
      data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
    }, {
      name: 'Manufacturing',
      data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
    }, {
      name: 'Sales & Distribution',
      data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
    }, {
      name: 'Project Development',
      data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
    }, {
      name: 'Other',
      data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
    }],
  
    responsive: {
      rules: [{
        condition: {
          maxWidth: 500
        },
        chartOptions: {
          legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'
          }
        }
      }]
    }
  
  });