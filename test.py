import pygame
import sys
import random
from enum import Enum
from dataclasses import dataclass

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 60
GRID_SIZE = 6
COMMAND_PANEL_HEIGHT = 120
WINDOW_WIDTH = CELL_SIZE * GRID_SIZE
WINDOW_HEIGHT = CELL_SIZE * GRID_SIZE + COMMAND_PANEL_HEIGHT
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

@dataclass
class Command:
    direction: str
    color: tuple

class Direction(Enum):
    UP = "\U0001f600"
    DOWN = "⬇d"
    LEFT = "⬅l"
    RIGHT = "➡️r"

class Path:
    def __init__(self):
        self.start_pos = [0, 0]
        self.goal_pos = None
        self.obstacles = []
        self.generate_path()

    def generate_path(self):
        # Generate a random goal position
        self.goal_pos = [random.randint(3, GRID_SIZE-1), random.randint(3, GRID_SIZE-1)]
        
        # Generate obstacles avoiding the path
        self.obstacles = []
        possible_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        possible_positions.remove((self.start_pos[0], self.start_pos[1]))
        possible_positions.remove((self.goal_pos[0], self.goal_pos[1]))
        
        # Add 3-5 obstacles
        for _ in range(random.randint(3, 5)):
            if possible_positions:
                pos = random.choice(possible_positions)
                self.obstacles.append([pos[0], pos[1]])
                possible_positions.remove(pos)

class GameState:
    def __init__(self):
        self.paths = self.generate_paths()
        self.current_path_index = 0
        self.current_path = self.paths[self.current_path_index]
        self.player_pos = self.current_path.start_pos.copy()
        self.commands = []
        self.current_command = 0
        self.is_playing = False
        self.game_won = False
        self.game_lost = False
        self.animation_timer = 0
        self.available_colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]

    def generate_paths(self):
        return [Path() for _ in range(5)]

    def next_path(self):
        self.current_path_index = (self.current_path_index + 1) % len(self.paths)
        self.current_path = self.paths[self.current_path_index]
        self.reset()

    def reset(self):
        self.player_pos = self.current_path.start_pos.copy()
        self.commands = []
        self.current_command = 0
        self.is_playing = False
        self.game_won = False
        self.game_lost = False
        self.animation_timer = 0

    def add_command(self, direction, color):
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

        # Check if move is valid
        if (0 <= new_pos[0] < GRID_SIZE and 
            0 <= new_pos[1] < GRID_SIZE and 
            new_pos not in self.current_path.obstacles):
            self.player_pos = new_pos
            
            # Check win/lose conditions
            if self.player_pos == self.current_path.goal_pos:
                self.game_won = True
                self.is_playing = False
            elif self.player_pos in self.current_path.obstacles:
                self.game_lost = True
                self.is_playing = False
        else:
            self.game_lost = True
            self.is_playing = False

        self.current_command += 1

class CommandPanel:
    def __init__(self, y_position):
        self.y_position = y_position
        self.button_size = 50
        self.spacing = 10
        self.direction_buttons = self.create_direction_buttons()
        self.color_buttons = self.create_color_buttons()
        # self.play_button = pygame.Rect(WINDOW_WIDTH - 60, 
        #                              self.y_position + 10, 40, 40)
        self.play_button = pygame.image.load("play.png")

    def create_direction_buttons(self):
        buttons = {}
        x_start = 10
        y = self.y_position + 10
        for direction in Direction:
            buttons[direction] = pygame.Rect(x_start, y, 
                                          self.button_size, self.button_size)
            x_start += self.button_size + self.spacing
        return buttons

    def create_color_buttons(self):
        buttons = []
        x_start = 10
        y = self.y_position + self.button_size + 20
        for color in [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]:
            buttons.append((pygame.Rect(x_start, y, 
                                     self.button_size, self.button_size), color))
            x_start += self.button_size + self.spacing
        return buttons

def draw_game(screen, game_state, command_panel):
    screen.fill(WHITE)
    
    # Draw grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Draw obstacles
    for obstacle in game_state.current_path.obstacles:
        pygame.draw.rect(screen, RED,
                        (obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))

    # Draw goal
    pygame.draw.rect(screen, GREEN,
                    (game_state.current_path.goal_pos[0] * CELL_SIZE, 
                     game_state.current_path.goal_pos[1] * CELL_SIZE,
                     CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.circle(screen, BLUE,
                      (game_state.player_pos[0] * CELL_SIZE + CELL_SIZE//2,
                       game_state.player_pos[1] * CELL_SIZE + CELL_SIZE//2),
                      CELL_SIZE//3)

    # Draw command panel
    for direction, button in command_panel.direction_buttons.items():
        pygame.draw.rect(screen, BLACK, button, 2)
        text = pygame.font.Font(None, 36).render(direction.value, True, BLACK)
        screen.blit(text, (button.centerx - text.get_width()//2,
                          button.centery - text.get_height()//2))

    for button, color in command_panel.color_buttons:
        pygame.draw.rect(screen, color, button)
        pygame.draw.rect(screen, BLACK, button, 2)

    # Draw play button (missile icon)
    pygame.draw.rect(screen, GREEN, command_panel.play_button)
    pygame.draw.polygon(screen, BLACK, [
        (command_panel.play_button.centerx - 10, command_panel.play_button.centery),
        (command_panel.play_button.centerx + 10, command_panel.play_button.centery),
        (command_panel.play_button.centerx, command_panel.play_button.centery - 15)
    ])

    # Draw command sequence
    x_start = 10
    y = WINDOW_HEIGHT - 40
    for command in game_state.commands:
        pygame.draw.circle(screen, command.color, (x_start + 15, y), 15)
        text = pygame.font.Font(None, 24).render(command.direction.value, True, BLACK)
        screen.blit(text, (x_start + 5, y - 10))
        x_start += 40

def main():
    game_state = GameState()
    command_panel = CommandPanel(GRID_SIZE * CELL_SIZE)
    clock = pygame.time.Clock()
    selected_color = BLUE
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_state.is_playing:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check direction buttons
                for direction, button in command_panel.direction_buttons.items():
                    if button.collidepoint(mouse_pos):
                        game_state.add_command(direction, selected_color)

                # Check color buttons
                for button, color in command_panel.color_buttons:
                    if button.collidepoint(mouse_pos):
                        selected_color = color

                # Check play button
                if command_panel.play_button.collidepoint(mouse_pos):
                    game_state.is_playing = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset game
                    game_state.reset()
                elif event.key == pygame.K_n:  # Next path
                    game_state.next_path()

        # Update game state
        if game_state.is_playing:
            game_state.animation_timer += 1
            if game_state.animation_timer >= 30:  # Move every 30 frames
                game_state.execute_next_command()
                game_state.animation_timer = 0

        # Draw game state
        draw_game(SCREEN, game_state, command_panel)

        # Display win/lose messages
        if game_state.game_won or game_state.game_lost:
            font = pygame.font.Font(None, 36)
            if game_state.game_won:
                text = font.render("You Win! 🌟", True, GREEN)
            else:
                text = font.render("Try Again! \U0001f600", True, RED)
            SCREEN.blit(text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()