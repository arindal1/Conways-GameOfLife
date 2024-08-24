import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Get the display info for full-screen mode
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Conway's Game of Life")

# Hide the cursor
pygame.mouse.set_visible(False)

# Set colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Cell size
cell_size = 5  # Updated cell size for larger cells

# Grid size
cols = screen_width // cell_size
rows = screen_height // cell_size

def create_random_grid(rows, cols, p_alive=0.1):
    """Create a grid with random cells."""
    return np.random.choice([0, 1], size=(rows, cols), p=[1 - p_alive, p_alive])

def update_grid(grid):
    # Use numpy's efficient array operations for speed
    neighbors = (
        np.roll(grid, 1, 0) + np.roll(grid, -1, 0) +
        np.roll(grid, 1, 1) + np.roll(grid, -1, 1) +
        np.roll(np.roll(grid, 1, 0), 1, 1) + np.roll(np.roll(grid, 1, 0), -1, 1) +
        np.roll(np.roll(grid, -1, 0), 1, 1) + np.roll(np.roll(grid, -1, 0), -1, 1)
    )

    # Apply Conway's rules
    new_grid = (neighbors == 3) | ((grid == 1) & (neighbors == 2))
    return new_grid.astype(int)

def draw_grid(screen, grid):
    # Create a surface for drawing to optimize performance
    surface = pygame.Surface((screen_width, screen_height))
    for y in range(rows):
        for x in range(cols):
            if grid[y, x] == 1:
                pygame.draw.rect(surface, GREEN, (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))
    # Blit the surface onto the screen in one operation
    screen.blit(surface, (0, 0))

# Initial grid setup
grid = create_random_grid(rows, cols)

# Main loop
running = True
clock = pygame.time.Clock()  # Create a clock object to control the frame rate

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Regenerate the grid with a new random seed
                grid = create_random_grid(rows, cols)

    # Update grid and draw it
    grid = update_grid(grid)
    screen.fill(BLACK)  # Clear the screen before drawing
    draw_grid(screen, grid)

    # Refresh the screen
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 frames per second

# Show the cursor again
pygame.mouse.set_visible(True)

# Quit Pygame
pygame.quit()
sys.exit()
