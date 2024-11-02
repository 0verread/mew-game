import pygame

class ButtonImage:
  def __init__(self, img_path, size=(50, 50)):
    # Load and scale the image
    self.original_img = pygame.image.load(img_path)
    self.image = pygame.transform.scale(self.original_img, size)
    self.rect = self.image.get_rect()
  def set_position(self, x, y):
    self.rect.x = x
    self.rect.y = y