import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up grid
ROWS, COLS = 17, 30
TILE_SIZE = WIDTH // COLS

# Pac-Man settings
pacman_pos = [1, 1]
pacman_dir = [0, 0]

# Ghost settings
ghosts = [
    {"pos": [28, 15], "dir": [0, 0], "color": RED},
    {"pos": [1, 15], "dir": [0, 0], "color": BLUE}
]

# Food settings
food = []

# Maze (1 for walls, 0 for paths)
maze = [
    "111111111111111111111111111111",
    "100000000011000000001100000001",
    "101111011111011111101111011101",
    "100000000000000000000000000001",
    "101111011111011111101111011101",
    "100000000011000000001100000001",
    "101111011111011111101111011101",
    "100000000000000000000000000001",
    "101111011111011111101111011101",
    "100000000011000000001100000001",
    "101111011111011111101111011101",
    "100000000000000000000000000001",
    "101111011111011111101111011101",
    "100000000011000000001100000001",
    "101111011111011111101111011101",
    "100000000000000000000000000001",
    "111111111111111111111111111111",
]

# Convert maze to a grid of walls and food
for row in range(ROWS):
    for col in range(COLS):
        if maze[row][col] == "0":
            food.append((col, row))

def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == "1":
                pygame.draw.rect(WIN, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif (col, row) in food:  # Draw food only if it's still in the food list
                pygame.draw.circle(WIN, WHITE, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), 3)

def draw_pacman():
    pygame.draw.circle(WIN, YELLOW, (pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2, pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 2)

def draw_ghosts():
    for ghost in ghosts:
        pygame.draw.circle(WIN, ghost["color"], (ghost["pos"][0] * TILE_SIZE + TILE_SIZE // 2, ghost["pos"][1] * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 2)

def move_pacman():
    new_pos = [pacman_pos[0] + pacman_dir[0], pacman_pos[1] + pacman_dir[1]]
    if maze[new_pos[1]][new_pos[0]] != "1":
        pacman_pos[0], pacman_pos[1] = new_pos[0], new_pos[1]
        if (new_pos[0], new_pos[1]) in food:
            food.remove((new_pos[0], new_pos[1]))

def move_ghosts():
    for ghost in ghosts:
        directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]  # Up, Down, Left, Right
        random.shuffle(directions)  # Randomize direction choice
        for direction in directions:
            new_pos = [ghost["pos"][0] + direction[0], ghost["pos"][1] + direction[1]]
            if maze[new_pos[1]][new_pos[0]] != "1":  # Check for walls
                ghost["pos"] = new_pos
                break

def check_collision():
    for ghost in ghosts:
        if pacman_pos == ghost["pos"]:
            return True
    return False

def show_game_over():
    font = pygame.font.SysFont(None, 55)
    text = font.render("You Lost!", True, RED)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    clock = pygame.time.Clock()

    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman_dir[0], pacman_dir[1] = -1, 0
                elif event.key == pygame.K_RIGHT:
                    pacman_dir[0], pacman_dir[1] = 1, 0
                elif event.key == pygame.K_UP:
                    pacman_dir[0], pacman_dir[1] = 0, -1
                elif event.key == pygame.K_DOWN:
                    pacman_dir[0], pacman_dir[1] = 0, 1

        move_pacman()
        move_ghosts()

        if check_collision():
            show_game_over()
            pygame.quit()
            sys.exit()

        # Draw everything
        WIN.fill(BLACK)
        draw_maze()
        draw_pacman()
        draw_ghosts()

        pygame.display.flip()

if __name__ == "__main__":
    main()
