const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const cellSize = 5; // Reduced cell size for smaller cells
const rows = Math.floor(canvas.height / cellSize);
const cols = Math.floor(canvas.width / cellSize);

let grid = createGrid();
let running = false;

function createGrid() {
    return new Array(rows).fill(null).map(() => new Array(cols).fill(0));
}

function randomizeGrid() {
    return grid.map(row => row.map(() => (Math.random() > 0.7 ? 1 : 0)));
}

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    grid.forEach((row, y) => {
        row.forEach((cell, x) => {
            ctx.fillStyle = cell ? '#00ff00' : '#000';
            ctx.fillRect(x * cellSize, y * cellSize, cellSize - 1, cellSize - 1);
        });
    });
}

function updateGrid() {
    const newGrid = grid.map(arr => [...arr]);

    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const neighbors = getNeighborCount(x, y);
            if (grid[y][x] === 1 && (neighbors < 2 || neighbors > 3)) {
                newGrid[y][x] = 0;
            } else if (grid[y][x] === 0 && neighbors === 3) {
                newGrid[y][x] = 1;
            }
        }
    }

    grid = newGrid;
    drawGrid();
}

function getNeighborCount(x, y) {
    let count = 0;
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            if (i === 0 && j === 0) continue;
            const col = (x + i + cols) % cols;
            const row = (y + j + rows) % rows;
            count += grid[row][col];
        }
    }
    return count;
}

function gameLoop() {
    if (running) {
        updateGrid();
        requestAnimationFrame(gameLoop);
    }
}

document.getElementById('startButton').addEventListener('click', () => {
    running = !running;
    if (running) {
        gameLoop();
    }
});

document.getElementById('resetButton').addEventListener('click', () => {
    grid = createGrid();
    drawGrid();
    running = false;
});

document.getElementById('randomizeButton').addEventListener('click', () => {
    grid = randomizeGrid();
    drawGrid();
});

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    drawGrid();
});

drawGrid();
