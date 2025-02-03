# V2/main.py
import pygame
from utils import logger
from cat import Cat
from house import House
from ball import Ball

# Pygame'i başlat
pygame.init()

# Pencere boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Başlık
pygame.display.set_caption("ScreenAnimals")

# Saat
clock = pygame.time.Clock()

# Objeleri oluştur
cat = Cat(100, 400)
house = House(500, 350)

# Top için sprite grubu
balls = pygame.sprite.Group()
ball = Ball(150, 30)
balls.add(ball)

# Oyun döngüsü
running = True
last_mouse_pos = None  # Farenin son konumunu saklamak için değişken
cat_walking_to_ball = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Kedi olayları işleme
        cat.handle_event(event)

        # Ev olayları işleme
        house.handle_event(event, balls, cat)

        # Top olayları işleme
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for ball in balls:
                if ball.rect.collidepoint(event.pos):
                    ball.dragging = True
                    ball.velocity = [0, 0]
                    last_mouse_pos = event.pos  # Farenin son konumunu kaydet
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for ball in balls:
                if ball.dragging:
                    ball.dragging = False
                    if last_mouse_pos:
                        # Farenin son konumu ile şimdiki konumu arasındaki farkı kullanarak hızı hesapla
                        dx = event.pos[0] - last_mouse_pos[0]
                        dy = event.pos[1] - last_mouse_pos[1]
                        ball.velocity = [dx / 5, dy / 5]  # Hızı ölçekle (daha yavaş hareket için)
                    last_mouse_pos = None  # Farenin son konumunu sıfırla
        elif event.type == pygame.MOUSEMOTION:
            for ball in balls:
                if ball.dragging:
                    ball.rect.center = event.pos
                    if last_mouse_pos:
                        # Top sürüklenirken farenin son konumunu güncelle
                        last_mouse_pos = event.pos

        # Sağ tıklama menüsü işlemleri
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Sağ tıklama
                if cat.rect.collidepoint(event.pos):
                    cat.show_menu = True

            elif event.button == 1: # Sol tıklama
                if cat.show_menu:
                    if not (cat.rect.right <= event.pos[0] <= cat.rect.right + 150 and cat.rect.top <= event.pos[1] <= cat.rect.top + 100): # Eğer menü dışına tıklanırsa
                        cat.show_menu = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if cat.show_menu:
                    cat.handle_menu_click(event.pos, house)

    # Objelerin durumunu güncelle
    cat.update(house)
    balls.update()
    for ball in balls:
        if not (0 <= ball.rect.x <= screen_width and 0 <= ball.rect.y <= screen_height):
            logger.warning(f"Top ekran dışında! Konum: {ball.rect.topleft}")

    # Kedi topa doğru yürüyecek mi?
    if len(balls) > 0:
        nearest_ball = cat.find_nearest_ball(balls)
        if nearest_ball:
            cat.walk_to_target(nearest_ball.rect.centerx, nearest_ball.rect.centery)
            # Top yakalandı mı?
            if cat.rect.colliderect(nearest_ball.rect):
                balls.remove(nearest_ball)
                cat.walking_animation = False

    # Kedinin konumu değiştiğinde menüyü kapat
    if cat.dragging:
        cat.show_menu = False

    # Ekranı temizle
    screen.fill((255, 255, 255))

    # Objeleri çiz
    balls.draw(screen)
    house.draw(screen)
    cat.draw(screen)

    # Kedinin menüsünü çiz (eğer gösteriliyorsa)
    if cat.show_menu:
        cat.draw_menu(screen, cat.rect.right, cat.rect.top)

    # Ekranı güncelle
    pygame.display.flip()

    # FPS
    clock.tick(60)

# Pygame'i sonlandır
pygame.quit()
logger.info("Oyun kapatıldı.")