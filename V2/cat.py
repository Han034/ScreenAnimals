import pygame
from utils import logger
import math

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("V2/assets/cat.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() // 4, self.original_image.get_height() // 4))
        self.rect = self.original_image.get_rect(topleft=(x, y))
        self.hunger = 100
        self.happiness = 100
        self.sleep = 100
        self.is_sleeping = False
        self.dragging = False
        self.is_inside_house = False
        self.show_menu = False
        self.walking_animation = False
        self.animation_counter = 0
        self.animation_speed = 5  # Daha düşük değer daha hızlı animasyon
        self.walking_images = [
            pygame.transform.scale(pygame.image.load("V2/assets/cat_walking.png").convert_alpha(), (self.original_image.get_width(), self.original_image.get_height())),
            pygame.transform.scale(pygame.image.load("V2/assets/cat_walking2.png").convert_alpha(), (self.original_image.get_width(), self.original_image.get_height()))
        ]
        self.current_walking_image = 0
        self.image = self.original_image  # Başlangıçta orijinal görseli kullan

    def update(self, house):
        if self.is_sleeping:
            self.sleep = max(0, self.sleep - 0.05)
            self.is_inside_house = True
        else:
            self.hunger = max(0, self.hunger - 0.01)
            self.sleep = min(100, self.sleep + 0.02)
            self.is_inside_house = False

        if self.hunger < 30 or self.sleep > 70:
            self.happiness = max(0, self.happiness - 0.03)
        else:
            self.happiness = min(100, self.happiness + 0.01)

        if self.rect.colliderect(house.rect):
            self.is_inside_house = True

        shrink_amount = 5
        extended_house_rect = house.rect.inflate(-shrink_amount, -shrink_amount)
        if not extended_house_rect.colliderect(self.rect):
            self.is_inside_house = False

        if self.walking_animation:
            #print("Kedinin yürüme animasyonu aktif")
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_walking_image = (self.current_walking_image + 1) % len(self.walking_images)
                self.image = self.walking_images[self.current_walking_image]
        else:
            #print("Kedinin yürüme animasyonu kapalı")
            self.image = self.original_image  # Animasyon yoksa orijinal görseli kullan

        #logger.info(f"Kedi Durumu - Açlık: {self.hunger}, Mutluluk: {self.happiness}, Uyku: {self.sleep}, Evin içinde mi: {self.is_inside_house}")

    def walk_to_target(self, target_x, target_y):
        """Kediyi belirli bir hedefe doğru yürütür."""
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery

        # Hedefe çok yakınsa hareketi durdur ve animasyonu sıfırla
        if abs(dx) < 1 and abs(dy) < 1:
            self.walking_animation = False
            self.animation_counter = 0
            self.current_walking_image = 0
            self.image = self.original_image
            print("Kedi hedefe ulaştı, animasyon durduruldu.")
            return

        self.walking_animation = True  # Yürüme animasyonunu başlat

        # X ve Y yönünde hareket et
        if dx > 0:
            self.rect.x += min(dx, 2)  # Sağa doğru yürü, hız 2
        elif dx < 0:
            self.rect.x += max(dx, -2)  # Sola doğru yürü, hız 2
        if dy > 0:
            self.rect.y += min(dy, 2)  # Aşağı doğru yürü, hız 2
        elif dy < 0:
            self.rect.y += max(dy, -2)  # Yukarı doğru yürü, hız 2  # Yukarı doğru yürü, hız 2

    def find_nearest_ball(self, balls):
        """En yakın topu bulur ve döndürür."""
        min_distance = float('inf')
        nearest_ball = None
        for ball in balls:
            dx = ball.rect.centerx - self.rect.centerx
            dy = ball.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance < min_distance:
                min_distance = distance
                nearest_ball = ball
        return nearest_ball

    def draw_menu(self, screen, x, y):
        """Kedinin sağ tıklama menüsünü çizer."""
        menu_width = 150
        menu_height = 100
        menu_x = x
        menu_y = y

        # Menü arkaplanı
        pygame.draw.rect(screen, (200, 200, 200), (menu_x, menu_y, menu_width, menu_height))

        font = pygame.font.Font(None, 20)

        # Açlık
        hunger_text = font.render(f"Açlık: {int(self.hunger)}", True, (0, 0, 0))
        screen.blit(hunger_text, (menu_x + 10, menu_y + 10))
        pygame.draw.rect(screen, (0, 0, 0), (menu_x + menu_width - 30, menu_y + 10, 20, 20), 2) # Kare buton

        # Mutluluk
        happiness_text = font.render(f"Mutluluk: {int(self.happiness)}", True, (0, 0, 0))
        screen.blit(happiness_text, (menu_x + 10, menu_y + 40))
        pygame.draw.rect(screen, (0, 0, 0), (menu_x + menu_width - 30, menu_y + 40, 20, 20), 2) # Kare buton

        # Uyku
        sleep_text = font.render(f"Uyku: {int(self.sleep)}", True, (0, 0, 0))
        screen.blit(sleep_text, (menu_x + 10, menu_y + 70))
        pygame.draw.rect(screen, (0, 0, 0), (menu_x + menu_width - 30, menu_y + 70, 20, 20), 2) # Kare buton

    def handle_menu_click(self, pos, house):
        """Menüdeki tıklamaları işler."""
        menu_x = self.rect.right
        menu_y = self.rect.top
        menu_width = 150
        # Açlık butonuna tıklandıysa
        if pygame.Rect(menu_x + menu_width - 30, menu_y + 10, 20, 20).collidepoint(pos):
            self.hunger = min(100, self.hunger + 20)
            logger.info("Açlık butonuna tıklandı. Yeni açlık değeri: " + str(self.hunger))

        # Uyku butonuna tıklandıysa
        elif pygame.Rect(menu_x + menu_width - 30, menu_y + 70, 20, 20).collidepoint(pos):
            self.sleep_mode(house)
            logger.info("Uyku butonuna tıklandı.")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            logger.info("MOUSEBUTTONDOWN olayı gerçekleşti - Cat")
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
            elif event.button == 3:
                if self.rect.collidepoint(event.pos):
                    print("Kediye sağ tıklandı, menü açılacak")
                    self.show_menu = True
        elif event.type == pygame.MOUSEBUTTONUP:
            logger.info("MOUSEBUTTONUP olayı gerçekleşti - Cat")
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.center = event.pos
        return False

    def sleep_mode(self, house):
        """Kediyi uyku moduna geçirir."""
        if self.rect.colliderect(house.rect):
            self.is_sleeping = True
            self.is_inside_house = True
        else:
            self.walk_to_house(house)
            self.is_inside_house = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Çizim için self.image kullan