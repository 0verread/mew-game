import random
from utils.constants import CONSTANTS

class Path:
  def __init__(self):
    self.start_pos = [0, 0]
    self.goal_pos = None
    self.obstacles = []
    self.generate_path()

  def generate_path(self):
    # Generate a random goal position
    self.goal_pos = [random.randint(3, CONSTANTS.GRID_SIZE-1), random.randint(3, CONSTANTS.GRID_SIZE-1)]
    
    # Generate obstacles avoiding the path
    self.obstacles = []
    possible_positions = [(x, y) for x in range(CONSTANTS.GRID_SIZE) for y in range(CONSTANTS.GRID_SIZE)]
    possible_positions.remove((self.start_pos[0], self.start_pos[1]))
    possible_positions.remove((self.goal_pos[0], self.goal_pos[1]))
    
    for _ in range(random.randint(3, 5)):
      if possible_positions:
        pos = random.choice(possible_positions)
        self.obstacles.append([pos[0], pos[1]])
        possible_positions.remove(pos)