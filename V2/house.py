# house.py
import pygame
from utils import logger
from ball import Ball

class House(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("V2/assets/house.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width() // 4, original_image.get_height() // 4))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move_with_cat_inside(self, cat, dx, dy):
      """Evi hareket ettirir ve eğer kedi evin içindeyse kediyi de hareket ettirir."""
      self.rect.x += dx
      self.rect.y += dy
      if cat.is_inside_house:
        cat.rect.x += dx
        cat.rect.y += dy

    def handle_event(self, event, balls, cat):
        if event.type == pygame.MOUSEBUTTONDOWN:
            logger.info("MOUSEBUTTONDOWN olayı gerçekleşti - House")
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
            elif event.button == 3:
                if self.rect.collidepoint(event.pos):
                    print("Eve sağ tıklandı, top oluşturulacak")
                    top_x = self.rect.centerx
                    top_y = self.rect.centery
                    balls.add(Ball(top_x, top_y))
                    logger.info(f"Top oluşturuldu. Konum: ({top_x}, {top_y})")
        elif event.type == pygame.MOUSEBUTTONUP:
            logger.info("MOUSEBUTTONUP olayı gerçekleşti - House")
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
                self.move_with_cat_inside(cat, rel_x, rel_y)
        return False
    