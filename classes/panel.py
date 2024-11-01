import pygame

from classes.buttons import ButtonImage
from utils.directions import Direction
from utils.constants import CONSTANTS
from utils.colors import COLORS

WINDOW_WIDTH = CONSTANTS.CELL_SIZE * CONSTANTS.GRID_SIZE
WINDOW_HEIGHT = CONSTANTS.CELL_SIZE * CONSTANTS.GRID_SIZE + CONSTANTS.COMMAND_PANEL_HEIGHT

class CommandPanel:
  def __init__(self, y_position):
    self.y_position = y_position
    self.button_size = 50
    self.spacing = 10
    # Load direction button images
    self.direction_buttons = {}
    for direction in Direction:
      image_path = f"{direction.value}.png"  # e.g., "up.png", "down.png", etc.
      button = ButtonImage(image_path, (self.button_size, self.button_size))
      x_start = 10 + (len(self.direction_buttons) * (self.button_size + self.spacing))
      button.set_position(x_start, y_position + 10)
      self.direction_buttons[direction] = button

    # Load play button
    self.play_button = ButtonImage("play.png", (40, 40))
    self.play_button.set_position(WINDOW_WIDTH - 60, y_position + 10)

    # Create color buttons (these remain as rectangles)
    self.color_buttons = self.create_color_buttons()

    def create_color_buttons(self):
        buttons = []
        x_start = 10
        y = self.y_position + self.button_size + 20
        for color in [COLORS.RED, COLORS.BLUE, COLORS.GREEN, COLORS.YELLOW, COLORS.PURPLE, COLORS.ORANGE]:
            buttons.append((pygame.Rect(x_start, y, 
                                     self.button_size, self.button_size), color))
            x_start += self.button_size + self.spacing
        return buttons