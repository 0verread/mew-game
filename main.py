import pygame
from classes.game import game

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

# @dataclass
# class Command:
#     direction: str
#     color: tuple

# class Direction(Enum):
#     UP = "up"
#     DOWN = "down"
#     LEFT = "left"
#     RIGHT = "right"

# class ButtonImage:
#     def __init__(self, image_path, size=(50, 50)):
#         # Load and scale the image
#         self.original_image = pygame.image.load(image_path)
#         self.image = pygame.transform.scale(self.original_image, size)
#         self.rect = self.image.get_rect()

#     def set_position(self, x, y):
#         self.rect.x = x
#         self.rect.y = y


class CommandPanel:
    def __init__(self, y_position):
        self.y_position = y_position
        self.button_size = 30
        self.spacing = 10
        
        # Load direction button images
        self.direction_buttons = {}
        for direction in Direction:
            image_path = f"./assets/{direction.value}.svg"  # e.g., "up.png", "down.png", etc.
            button = ButtonImage(image_path, (self.button_size, self.button_size))
            x_start = 10 + (len(self.direction_buttons) * (self.button_size + self.spacing))
            button.set_position(x_start, y_position + 10)
            self.direction_buttons[direction] = button

        # Load play button
        self.play_button = ButtonImage("./assets/play.png", (40, 40))
        self.play_button.set_position(WINDOW_WIDTH - 60, y_position + 10)

        # Create color buttons (these remain as rectangles)
        self.color_buttons = self.create_color_buttons()

    def create_color_buttons(self):
        buttons = []
        x_start = 10
        y = self.y_position + self.button_size + 20
        for color in [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]:
            buttons.append((pygame.Rect(x_start, y, 
                                     self.button_size, self.button_size), color))
            x_start += self.button_size + self.spacing
        return buttons



if __name__ == "__main__":
    game()