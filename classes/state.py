from dataclasses import dataclass
from classes.path import Path
from utils.colors import COLORS
from utils.directions import Direction
from utils.constants import CONSTANTS


@dataclass
class Command:
    direction: str
    color: tuple

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
    self.available_colors = [COLORS.RED, COLORS.BLUE, COLORS.GREEN, COLORS.YELLOW, COLORS.PURPLE, COLORS.ORANGE]

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
    if (0 <= new_pos[0] < CONSTANTS.GRID_SIZE and 
        0 <= new_pos[1] < CONSTANTS.GRID_SIZE and 
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
