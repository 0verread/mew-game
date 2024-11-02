import sys
import pygame

from classes.state import GameState
from classes.panel import CommandPanel
from utils.constants import CONSTANTS
from utils.colors import COLORS
# Initialize Pygame
pygame.init()

WINDOW_WIDTH = CONSTANTS.CELL_SIZE * CONSTANTS.GRID_SIZE
WINDOW_HEIGHT = CONSTANTS.CELL_SIZE * CONSTANTS.GRID_SIZE + CONSTANTS.COMMAND_PANEL_HEIGHT
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Toddler Programming Game")

def draw_game(screen, game_state, command_panel):
  screen.fill(COLORS.WHITE)
    
  # Draw grid
  for x in range(CONSTANTS.GRID_SIZE):
    for y in range(CONSTANTS.GRID_SIZE):
      pygame.draw.rect(screen, COLORS.BLACK, 
                          (x * CONSTANTS.CELL_SIZE, 
                           y * CONSTANTS.CELL_SIZE, 
                           CONSTANTS.CELL_SIZE, 
                           CONSTANTS.CELL_SIZE), 1)

  # Draw obstacles
  for obstacle in game_state.current_path.obstacles:
    pygame.draw.rect(screen, COLORS.RED,
                      (obstacle[0] * CONSTANTS.CELL_SIZE, 
                       obstacle[1] * CONSTANTS.CELL_SIZE, 
                        CONSTANTS.CELL_SIZE, 
                        CONSTANTS.CELL_SIZE))

  # Draw goal
  pygame.draw.rect(screen, COLORS.GREEN,
                  (game_state.current_path.goal_pos[0] * CONSTANTS.CELL_SIZE, 
                    game_state.current_path.goal_pos[1] * CONSTANTS.CELL_SIZE,
                    CONSTANTS.CELL_SIZE, 
                    CONSTANTS.CELL_SIZE))

  # Draw player
  pygame.draw.circle(screen, COLORS.BLUE,
                    (game_state.player_pos[0] * CONSTANTS.CELL_SIZE + CONSTANTS.CELL_SIZE//2,
                      game_state.player_pos[1] * CONSTANTS.CELL_SIZE + CONSTANTS.CELL_SIZE//2),
                    CONSTANTS.CELL_SIZE//3)

  # Draw direction buttons (images)
  for button in command_panel.direction_buttons.values():
    screen.blit(button.image, button.rect)

  # Draw play button (image)
  screen.blit(command_panel.play_button.image, command_panel.play_button.rect)

  # Draw color buttons
  for button, color in command_panel.color_buttons:
    pygame.draw.rect(screen, color, button)
    pygame.draw.rect(screen, COLORS.BLACK, button, 2)

  # Draw command sequence
  x_start = 10
  y = WINDOW_HEIGHT - 40
  for command in game_state.commands:
    pygame.draw.circle(screen, command.color, (x_start + 15, y), 15)
    # Load and draw the corresponding direction image for the command
    direction_img = command_panel.direction_buttons[command.direction].image
    small_direction_img = pygame.transform.scale(direction_img, (30, 30))
    screen.blit(small_direction_img, (x_start, y - 15))
    x_start += 40

def game():
  game_state = GameState()
  command_panel = CommandPanel(CONSTANTS.GRID_SIZE * CONSTANTS.CELL_SIZE)
  clock = pygame.time.Clock()
  selected_color = COLORS.BLUE
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        
      if event.type == pygame.MOUSEBUTTONDOWN and not game_state.is_playing:
        mouse_pos = pygame.mouse.get_pos()
            
        # Check direction buttons
        for direction, button in command_panel.direction_buttons.items():
          if button.rect.collidepoint(mouse_pos):
            game_state.add_command(direction, selected_color)

        # Check color buttons
        for button, color in command_panel.color_buttons:
          if button.collidepoint(mouse_pos):
            selected_color = color

        # Check play button
        if command_panel.play_button.rect.collidepoint(mouse_pos):
          game_state.is_playing = True

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:  # Reset game
          game_state.reset()
        elif event.key == pygame.K_n:  # Next path
          game_state.next_path()

    # Update game state
    if game_state.is_playing:
      game_state.animation_timer += 1
      if game_state.animation_timer >= 30:
        game_state.execute_next_command()
        game_state.animation_timer = 0

    # Draw game state
    draw_game(SCREEN, game_state, command_panel)

    # Display win/lose messages
    if game_state.game_won or game_state.game_lost:
        font = pygame.font.Font(None, 36)
        if game_state.game_won:
            text = font.render("You Win!", True, COLORS.GREEN)
        else:
            text = font.render("Try Again! ", True, COLORS.RED)
        SCREEN.blit(text, (WINDOW_WIDTH//4, WINDOW_HEIGHT//2))

    pygame.display.flip()
    clock.tick(30)