# ball.py
import pygame
from utils import logger

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("V2/assets/ball.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (original_image.get_width() // 40, original_image.get_height() // 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.dragging = False
        self.velocity = [0, 0]
        self.gravity = 0.5  # Yerçekimi ivmesi
        self.bounce = 0.7  # Sekme katsayısı
        self.friction = 0.99  # Sürtünme katsayısı

    def update(self):
        if not self.dragging:
            # Yerçekimi etkisi
            self.velocity[1] += self.gravity

            # Hareket
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]

            # Sürtünme etkisi (sadece yerdeyken)
            if self.rect.bottom >= 550:  # 550 zeminin y koordinatı
                self.velocity[0] *= self.friction
                if abs(self.velocity[0]) < 0.1:  # Çok yavaşsa durdur
                    self.velocity[0] = 0

            # Zeminle çarpışma kontrolü
            if self.rect.bottom >= 550:
                self.rect.bottom = 550
                self.velocity[1] = -self.velocity[1] * self.bounce  # Sekme

                # Sekme sonrası çok düşük hızları sıfırla (titremeyi önlemek için)
                if abs(self.velocity[1]) < 2:
                    self.velocity[1] = 0

            # Duvarlarla çarpışma kontrolü (sol ve sağ)
            if self.rect.left <= 0:
                self.rect.left = 0
                self.velocity[0] = -self.velocity[0] * self.bounce
            elif self.rect.right >= 800:  # 800 ekran genişliği
                self.rect.right = 800
                self.velocity[0] = -self.velocity[0] * self.bounce

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.center = event.pos
        return False