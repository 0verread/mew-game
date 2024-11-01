import pygame
import sys
import random
from enum import Enum
from dataclasses import dataclass
import time

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 60
GRID_SIZE = 6
BUTTON_HEIGHT = 80
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE
WINDOW_HEIGHT = CELL_SIZE * GRID_SIZE + BUTTON_HEIGHT
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Toddler Programming Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class Direction(Enum):
    UP = "⬆️"
    DOWN = "⬇️"
    LEFT = "⬅️"
    RIGHT = "➡️"

@dataclass
class Command:
    direction: Direction
    color: tuple

class Path:
    def __init__(self):
        self.start_pos = [0, 0]
        self.goal_pos = [0, 0]
        self.path_cells = []
        self.obstacles = []

    @staticmethod
    def generate_random_path():
        path = Path()
        path.start_pos = [0, random.randint(0, GRID_SIZE-1)]
        current_pos = path.start_pos.copy()
        path.path_cells = [current_pos.copy()]
        
        # Generate random path
        steps = random.randint(4, 8)
        for _ in range(steps):
            possible_moves = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x = current_pos[0] + dx
                new_y = current_pos[1] + dy
                if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and 
                    [new_x, new_y] not in path.path_cells):
                    possible_moves.append((dx, dy))
            
            if not possible_moves:
                break
                
            dx, dy = random.choice(possible_moves)
            current_pos[0] += dx
            current_pos[1] += dy
            path.path_cells.append(current_pos.copy())
        
        path.goal_pos = current_pos.copy()
        
        # Generate obstacles
        path.obstacles = []
        for _ in range(random.randint(3, 5)):
            while True:
                obs = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]
                if obs not in path.path_cells and obs not in path.obstacles:
                    path.obstacles.append(obs)
                    break
                    
        return path

class GameState:
    def __init__(self):
        self.paths = [Path.generate_random_path() for _ in range(5)]
        self.current_path_index = 0
        self.player_pos = None
        self.commands = []
        self.current_command = 0
        self.is_playing = False
        self.game_won = False
        self.game_lost = False
        self.reset_current_path()

    def reset_current_path(self):
        self.player_pos = self.paths[self.current_path_index].start_pos.copy()
        self.commands = []
        self.current_command = 0
        self.is_playing = False
        self.game_won = False
        self.game_lost = False

    def next_path(self):
        self.current_path_index = (self.current_path_index + 1) % len(self.paths)
        self.reset_current_path()

    def add_command(self, direction, color):
        if not self.is_playing:
            self.commands.append(Command(direction, color))

    def execute_next_command(self):
        if self.current_command >= len(self.commands):
            self.is_playing = False
            return

        command = self.commands[self.current_command]
        new_pos = self.player_pos.copy()
        
        if command.direction == Direction.UP:
            new_pos[1] -= 1
        elif command.direction == Direction.DOWN:
            new_pos[1] += 1
        elif command.direction == Direction.LEFT:
            new_pos[0] -= 1
        elif command.direction == Direction.RIGHT:
            new_pos[0] += 1

        if (0 <= new_pos[0] < GRID_SIZE and 
            0 <= new_pos[1] < GRID_SIZE and 
            new_pos not in self.paths[self.current_path_index].obstacles):
            self.player_pos = new_pos
            
            if self.player_pos == self.paths[self.current_path_index].goal_pos:
                self.game_won = True
                self.is_playing = False
            elif self.player_pos not in self.paths[self.current_path_index].path_cells:
                self.game_lost = True
                self.is_playing = False
        else:
            self.game_lost = True
            self.is_playing = False

        self.current_command += 1

class Button:
    def __init__(self, x, y, width, height, color, text="", icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.icon = icon
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        if self.text:
            text_surface = self.font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        
        if self.icon:
            icon_surface = self.font.render(self.icon, True, BLACK)
            icon_rect = icon_surface.get_rect(center=self.rect.center)
            screen.blit(icon_surface, icon_rect)

    def handle_click(self, pos):
        return self.rect.collidepoint(pos)

def draw_game(screen, game_state):
    screen.fill(WHITE)
    
    # Draw grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    current_path = game_state.paths[game_state.current_path_index]

    # Draw path (slightly visible)
    for cell in current_path.path_cells:
        pygame.draw.rect(screen, (*YELLOW, 128),
                        (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))

    # Draw obstacles
    for obstacle in current_path.obstacles:
        pygame.draw.rect(screen, RED,
                        (obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))

    # Draw goal
    pygame.draw.rect(screen, GREEN,
                    (current_path.goal_pos[0] * CELL_SIZE, 
                     current_path.goal_pos[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))

    # Draw player
    if game_state.player_pos:
        pygame.draw.circle(screen, BLUE,
                          (game_state.player_pos[0] * CELL_SIZE + CELL_SIZE//2,
                           game_state.player_pos[1] * CELL_SIZE + CELL_SIZE//2),
                          CELL_SIZE//3)

def main():
    game_state = GameState()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Create buttons
    button_width = 50
    button_spacing = 10
    button_y = WINDOW_HEIGHT - BUTTON_HEIGHT + 10
    
    direction_buttons = [
        Button(10, button_y, button_width, button_width, WHITE, icon="⬆️"),
        Button(10 + button_width + button_spacing, button_y, button_width, button_width, WHITE, icon="⬇️"),
        Button(10 + (button_width + button_spacing) * 2, button_y, button_width, button_width, WHITE, icon="⬅️"),
        Button(10 + (button_width + button_spacing) * 3, button_y, button_width, button_width, WHITE, icon="➡️"),
    ]
    
    color_buttons = [
        Button(10 + (button_width + button_spacing) * 4, button_y, button_width, button_width, RED),
        Button(10 + (button_width + button_spacing) * 5, button_y, button_width, button_width, BLUE),
        Button(10 + (button_width + button_spacing) * 6, button_y, button_width, button_width, GREEN),
    ]
    
    play_button = Button(10 + (button_width + button_spacing) * 7, button_y, button_width, button_width, WHITE, icon="▶️")
    reset_button = Button(10 + (button_width + button_spacing) * 8, button_y, button_width, button_width, WHITE, icon="🔄")

    last_move_time = 0
    move_delay = 500  # milliseconds

    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_state.is_playing:
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle direction buttons
                for i, button in enumerate(direction_buttons):
                    if button.handle_click(mouse_pos):
                        direction = list(Direction)[i]
                        game_state.add_command(direction, BLUE)  # Default color

                # Handle color buttons
                for button in color_buttons:
                    if button.handle_click(mouse_pos):
                        if game_state.commands:
                            game_state.commands[-1].color = button.color

                # Handle play button
                if play_button.handle_click(mouse_pos):
                    game_state.is_playing = True
                    game_state.current_command = 0

                # Handle reset button
                if reset_button.handle_click(mouse_pos):
                    game_state.reset_current_path()

        # Execute commands with delay
        if game_state.is_playing and current_time - last_move_time >= move_delay:
            game_state.execute_next_command()
            last_move_time = current_time

        # Draw game state
        draw_game(SCREEN, game_state)

        # Draw buttons
        for button in direction_buttons + color_buttons + [play_button, reset_button]:
            button.draw(SCREEN)

        # Draw command sequence
        command_y = WINDOW_HEIGHT - BUTTON_HEIGHT//2
        for i, command in enumerate(game_state.commands):
            pygame.draw.circle(SCREEN, command.color,
                            (10 + i * 25, command_y),
                            10)

        # Display win/lose messages
        if game_state.game_won:
            text = font.render("You Win! 🌟", True, GREEN)
            SCREEN.blit(text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2))
        elif game_state.game_lost:
            text = font.render("Try Again! \U0001f600", True, RED)
            SCREEN.blit(text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()