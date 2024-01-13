import pygame  # Import the pygame library for creating games.
import random  # Import the random library for generating random numbers.

pygame.init()  # Initialize all imported pygame modules.

GRID_SIZE = 10  # Set the size of the grid cells.
WINDOW = 50  # Set the number of grid cells in one row or column.
WIDTH, HEIGHT = GRID_SIZE * WINDOW, GRID_SIZE * WINDOW  # Calculate the width and height of the window.
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window.
pygame.display.set_caption("Game")  # Set the caption of the window.

# Define color constants and cube size.
WHITE, BLACK, COLOR, cube_size = (255, 255, 255), (0, 0, 0), (128, 0, 0), GRID_SIZE  

cube_pos = [WIDTH // 2, HEIGHT // 2]  # Set the starting position of the cube at the center of the window.
grid = [[False for _ in range(WINDOW)] for _ in range(WINDOW)]  # Initialize a 2D grid to keep track of filled cells.
show_grid = False  # Flag to toggle the visibility of the grid.
last_click = None  # Variable to store the position of the last click (not used in this code).

# Define a list of colors to cycle through.
color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 0, 255)]  
color_index = 0  # Index to keep track of the current color.

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            # Draw a rectangle in each grid cell, colored if the cell is filled.
            if grid[x // GRID_SIZE][y // GRID_SIZE]:
                pygame.draw.rect(screen, COLOR, (x, y, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE))
    # Draw grid lines if show_grid is True.
    if show_grid:
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_cube():
    current_color = color_list[color_index]  # Get the current color from the color list.
    # Draw the cube at its current position with the current color.
    pygame.draw.rect(screen, current_color, (*cube_pos, cube_size, cube_size))

def move_cube(direction):
    # Determine the axis of movement based on the direction.
    i = 0 if direction in ('LEFT', 'RIGHT') else 1
    # Calculate the new position of the cube.
    new_pos = cube_pos[i] + (GRID_SIZE if direction in ('DOWN', 'RIGHT') else -GRID_SIZE)
    # Check if the new position is within the window boundaries.
    if 0 <= new_pos < (WIDTH if i == 0 else HEIGHT):
        # Calculate the corresponding grid cell for the new position.
        next_grid_pos = (new_pos // GRID_SIZE, cube_pos[1-i] // GRID_SIZE) if i == 0 else (cube_pos[1-i] // GRID_SIZE, new_pos // GRID_SIZE)
        # Move the cube if the new grid cell is not filled.
        if not grid[next_grid_pos[0]][next_grid_pos[1]]:
            cube_pos[i] = new_pos

def toggle_block(mouse_pos):
    # Convert mouse position to grid coordinates.
    x, y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
    # Toggle the state of the clicked grid cell.
    try:
        grid[x][y] = True
    except:
        pass

running = True  # Flag to keep the game loop running.
while running:
    for event in pygame.event.get():
        # Handle different types of events.
        if event.type == pygame.QUIT:
            # End the game loop if the window is closed.
            running = False
        elif event.type == pygame.KEYDOWN:
            # Handle key presses.
            if event.key == pygame.K_g:
                # Toggle grid visibility.
                show_grid = not show_grid
            elif event.key == pygame.K_c:
                # Cycle through colors.
                color_index = (color_index + 1) % len(color_list)
            else:
                # Map keys to directions and move the cube accordingly.
                direction_map = {
                    pygame.K_UP: 'UP', pygame.K_DOWN: 'DOWN', 
                    pygame.K_LEFT: 'LEFT', pygame.K_RIGHT: 'RIGHT',
                    pygame.K_w: 'UP', pygame.K_s: 'DOWN', 
                    pygame.K_a: 'LEFT', pygame.K_d: 'RIGHT'
                }
                move_cube(direction_map.get(event.key))
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            # Handle mouse button presses and motion.
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                # Toggle a block on left click.
                toggle_block(pygame.mouse.get_pos())
            elif mouse_buttons[2]:
                # Erase a block on right click.
                x, y = pygame.mouse.get_pos()
                x, y = x // GRID_SIZE, y // GRID_SIZE
                grid[x][y] = False

    # Update the display.
    screen.fill(BLACK)  # Clear the screen.
    draw_grid()  # Draw the grid and filled cells.
    draw_cube()  # Draw the cube.
    pygame.display.flip()  # Update the full display Surface to the screen.
    pygame.time.delay(100)  # Wait a short time before the next loop iteration.

pygame.quit()  # Uninitialize all pygame modules and quit.
