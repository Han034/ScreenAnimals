import pygame
import random
import os

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(os.path.join("log", "Logger.log"), "a") as log_file:
        log_file.write(log_entry + "\n")
        
class Top:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.PIC_FOLDER = os.path.join(os.path.dirname(__file__), "..", "pic")
        self.image = pygame.image.load(os.path.join(self.PIC_FOLDER, "top.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))  # Topun boyutunu ayarlayın
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hiz_x = 0
        self.hiz_y = 0
        self.yercekimi = 0.5
        self.sekme_sayisi = 0
        self.hareket_basladi = False

    def ciz(self, screen):
        screen.blit(self.image, self.rect)

    def hareket_ettir(self):
        if self.hareket_basladi:
            self.hiz_y += self.yercekimi
            self.x += self.hiz_x
            self.y += self.hiz_y
            self.rect.topleft = (self.x, self.y)

            # Sekme kontrolü
            if self.rect.bottom >= self.screen_height:
                self.y = self.screen_height - self.rect.height
                self.hiz_y = -self.hiz_y * 0.8  # Sekme etkisi
                self.hiz_x *= 0.9 # Yatay hız sürtünme ile azalır
                self.sekme_sayisi += 1

                # Top durduğunda
                if self.sekme_sayisi > 5:  # Sekme sayısını sınırlayın
                    self.hareket_basladi = False
                    self.hiz_x = 0
                    self.hiz_y = 0

            # Ekranın yan sınırlarına çarpma kontrolü
            if self.rect.left <= 0 or self.rect.right >= self.screen_width:
                self.hiz_x = -self.hiz_x

    def rastgele_hareket_baslat(self):
        self.hareket_basladi = True
        self.hiz_x = random.randint(-5, 5) # Yatayda rastgele hız
        self.hiz_y = -random.randint(5, 10)  # Dikeyde rastgele hız (yukarı doğru)
        self.yercekimi = 0.3
        self.sekme_sayisi = 0

    def takip_et(self, hedef_x, hedef_y):
        # Kedinin topu takip etmesi için (şimdilik pasif)
        pass