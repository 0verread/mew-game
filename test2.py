import pygame
import random

# Constants
GRID_SIZE = 5
CELL_SIZE = 100
WINNING_POSITION = (0, GRID_SIZE - 1)
OBSTACLE_COUNT = 5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)
AGENT_COLOR = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Colorful Paths Adventure")
clock = pygame.time.Clock()

def generate_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    # Place obstacles
    for _ in range(OBSTACLE_COUNT):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while (x, y) == (GRID_SIZE - 1, 0) or grid[y][x] == 1:  # Avoid placing on the start position
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        grid[y][x] = 1  # Mark obstacle
    return grid

def draw_grid(grid, agent_pos):
    screen.fill(WHITE)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) == agent_pos:
                pygame.draw.rect(screen, AGENT_COLOR, rect)
            elif grid[y][x] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Draw grid lines

def main():
    agent_pos = (GRID_SIZE - 1, 0)
    grid = generate_grid()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and agent_pos[0] > 0:
                    agent_pos = (agent_pos[0] - 1, agent_pos[1])
                elif event.key == pygame.K_DOWN and agent_pos[0] < GRID_SIZE - 1:
                    agent_pos = (agent_pos[0] + 1, agent_pos[1])
                elif event.key == pygame.K_LEFT and agent_pos[1] > 0:
                    agent_pos = (agent_pos[0], agent_pos[1] - 1)
                elif event.key == pygame.K_RIGHT and agent_pos[1] < GRID_SIZE - 1:
                    agent_pos = (agent_pos[0], agent_pos[1] + 1)

                # Check win/lose condition
                if agent_pos == WINNING_POSITION:
                    print("You Win! 🎉")
                    running = False
                elif grid[agent_pos[0]][agent_pos[1]] == 1:
                    print("You Lose! 💔")
                    running = False
        
        draw_grid(grid, agent_pos)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
