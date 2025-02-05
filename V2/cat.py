import pygame
from utils import logger
import math
import time

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("V2/assets/cat.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hunger = 100
        self.happiness = 100
        self.sleep = 100
        self.is_sleeping = False
        self.dragging = False
        self.is_inside_house = False
        self.show_menu = False
        self.walking_animation = False
        self.animation_counter = 0
        self.animation_speed = 5
        self.walking_images_right = [
            pygame.transform.scale(pygame.image.load("V2/assets/cat_walking.png").convert_alpha(), (self.image.get_width(), self.image.get_height())),
            pygame.transform.scale(pygame.image.load("V2/assets/cat_walking2.png").convert_alpha(), (self.image.get_width(), self.image.get_height()))
        ]
        self.walking_images_left = [
            pygame.transform.scale(pygame.image.load("V2/assets/cat_walking_left.png").convert_alpha(), (self.image.get_width(), self.image.get_height())),
            pygame.transform.scale(pygame.image.load("V2/assets/cat_walking_left2.png").convert_alpha(), (self.image.get_width(), self.image.get_height()))
        ]
        self.current_walking_image = 0
        self.direction = "right"
        self.last_position = self.rect.center  # Son konumu sakla
        self.last_moved_time = time.time()  # Son hareket zamanını sakla

    def update(self, house,balls):
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

        # Yürüme animasyonu kontrolü
        if self.walking_animation:
            #print("Animasyon çalışıyor.")
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_walking_image = (self.current_walking_image + 1) % len(self.walking_images_right)
                if self.direction == "right":
                    self.image = self.walking_images_right[self.current_walking_image]
                elif self.direction == "left":
                    self.image = self.walking_images_left[self.current_walking_image]

            # Kedinin mevcut hızı
            dx = abs(self.rect.centerx - house.rect.centerx) # Evin merkezi ile aradaki mesafe (gereksiz, silinecek)
            dy = abs(self.rect.centery - house.rect.centery) # Evin merkezi ile aradaki mesafe (gereksiz, silinecek)

             # Eğer kedi hareket etmiyorsa ve animasyon açıksa, animasyonu durdur
            if self.rect.center == self.last_position:  # Eğer kedi hareket etmiyorsa
              if time.time() - self.last_moved_time > 1:  # ve 1 saniyeden fazla zaman geçmişse
                self.walking_animation = False
                self.animation_counter = 0
                self.current_walking_image = 0
                self.image = self.original_image
                logger.info("Kedi 1 saniyeden fazla süredir hareket etmedi, animasyon durduruldu ve takip fonksiyonu yeniden başlatılıyor.")
                # Topu takip fonksiyonunu yeniden başlat
                nearest_ball = self.find_nearest_ball(balls)
                if nearest_ball:
                  self.walk_to_target(nearest_ball.rect.centerx, nearest_ball.rect.centery)
            else:  # Eğer kedi hareket ediyorsa
              self.last_position = self.rect.center
              self.last_moved_time = time.time()
        else:
            #print("Kedinin yürüme animasyonu kapalı")
            self.image = self.original_image

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
            self.image = self.original_image  # Orijinal görsele dön
            print("Kedi hedefe ulaştı, animasyon durduruldu.")
            return

        self.walking_animation = True  # Yürüme animasyonunu başlat

        # X ve Y yönünde hareket et
        if dx > 0:
            self.rect.x += min(dx, 2)  # Sağa doğru yürü, hız 2
            self.direction = "right"
        elif dx < 0:
            self.rect.x += max(dx, -2)  # Sola doğru yürü, hız 2
            self.direction = "left"
        if dy > 0:
            self.rect.y += min(dy, 2)  # Aşağı doğru yürü, hız 2
        elif dy < 0:
            self.rect.y += max(dy, -2)  # Yukarı doğru yürü, hız 2

        self.last_position = self.rect.center  # Son konumu güncelle
        self.last_moved_time = time.time()  # Son hareket zamanını güncelle
        #print(f"Kedinin konumu güncellendi: ({self.rect.x}, {self.rect.y})")

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
        menu_height = 130  # Menü yüksekliğini artır
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

        # Özelleştir
        customize_text = font.render("Özelleştir", True, (0, 0, 0))
        screen.blit(customize_text, (menu_x + 10, menu_y + menu_height - 30))  # Özelleştir butonunu aşağı kaydır

    def handle_menu_click(self, pos, house,customization_menu):
         """Menüdeki tıklamaları işler."""
         global current_menu # current_menu ve CUSTOMIZATION_MENU değişkenlerini global olarak tanımla
         menu_x = self.rect.right
         menu_y = self.rect.top
         menu_width = 150
         menu_height = 130

         # Açlık butonuna tıklandıysa
         if pygame.Rect(menu_x + menu_width - 30, menu_y + 10, 20, 20).collidepoint(pos):
             self.hunger = min(100, self.hunger + 20)
             logger.info("Açlık butonuna tıklandı. Yeni açlık değeri: " + str(self.hunger))

         # Uyku butonuna tıklandıysa
         elif pygame.Rect(menu_x + menu_width - 30, menu_y + 70, 20, 20).collidepoint(pos):
             self.sleep_mode(house)
             logger.info("Uyku butonuna tıklandı.")
        
        # Özelleştirme butonuna tıklandıysa
         elif pygame.Rect(menu_x, menu_y + menu_height - 30, menu_width, 30).collidepoint(pos):
            current_menu = customization_menu  # Artık parametre olarak alıyoruz
            print(f"current_menu değeri (cat.py içinde): {current_menu}")  # Hata ayıklama için
            self.show_menu = False
            logger.info("Özelleştirme menüsüne geçildi.")

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