import pygame
from utils import logger
from cat import Cat
from house import House
from ball import Ball
import math

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

# Menü durumları
global MAIN_MENU, CUSTOMIZATION_MENU # Değişkenleri global olarak tanımla
MAIN_MENU = 0
CUSTOMIZATION_MENU = 1
current_menu = MAIN_MENU

# Renk seçenekleri
cat_colors = {
    "Sarı": (255, 255, 0),
    "Siyah": (0, 0, 0),
    "Beyaz": (255, 255, 255),
    "Gri": (128, 128, 128)
}
selected_color = "Sarı"  # Varsayılan renk

def draw_customization_menu(screen):
    """Özelleştirme menüsünü çizer."""
    menu_width = 300
    menu_height = 200
    menu_x = screen_width // 2 - menu_width // 2
    menu_y = screen_height // 2 - menu_height // 2

    # Menü arkaplanı
    pygame.draw.rect(screen, (255, 0, 0), (menu_x, menu_y, menu_width, menu_height))

    font = pygame.font.Font(None, 30)

    # Başlık
    title_text = font.render("Özelleştirme", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen_width // 2, menu_y + 30))
    screen.blit(title_text, title_rect)

    # Renk butonları
    button_y = menu_y + 80
    for color_name, color_value in cat_colors.items():
        button_rect = pygame.Rect(menu_x + 20, button_y, 100, 40)
        pygame.draw.rect(screen, color_value, button_rect)
        if selected_color == color_name:
            pygame.draw.rect(screen, (255, 0, 0), button_rect, 3)
        color_text = font.render(color_name, True, (0, 0, 0))
        color_text_rect = color_text.get_rect(center=button_rect.center)
        screen.blit(color_text, color_text_rect)
        button_y += 50

    # Geri butonu
    back_button_rect = pygame.Rect(menu_x + menu_width - 120, menu_y + menu_height - 50, 100, 40)
    pygame.draw.rect(screen, (100, 100, 100), back_button_rect)
    back_text = font.render("Geri", True, (0, 0, 0))
    back_text_rect = back_text.get_rect(center=back_button_rect.center)
    screen.blit(back_text, back_text_rect)

def handle_customization_menu_event(event):
    """Özelleştirme menüsündeki olayları işler."""
    global current_menu, selected_color

    menu_width = 300
    menu_height = 200
    menu_x = screen_width // 2 - menu_width // 2
    menu_y = screen_height // 2 - menu_height // 2

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            # Renk butonları
            button_y = menu_y + 80
            for color_name in cat_colors.keys():
                button_rect = pygame.Rect(menu_x + 20, button_y, 100, 40)
                if button_rect.collidepoint(event.pos):
                    selected_color = color_name
                    cat.change_color(cat_colors[selected_color])
                    break
                button_y += 50

            # Geri butonu
            back_button_rect = pygame.Rect(menu_x + menu_width - 120, menu_y + menu_height - 50, 100, 40)
            if back_button_rect.collidepoint(event.pos):
                current_menu = MAIN_MENU
                print("Ana menüye dönüldü.")

# Oyun döngüsü
running = True
last_mouse_pos = None
cat_walking_to_ball = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_menu == MAIN_MENU:
            # Kedi olayları işleme
            if cat.handle_event(event):
                continue

            # Ev olayları işleme
            if house.handle_event(event, balls, cat):
                continue

            # Top olayları işleme
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for ball in balls:
                    if ball.rect.collidepoint(event.pos):
                        ball.dragging = True
                        ball.velocity = [0, 0]
                        last_mouse_pos = event.pos
                        break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for ball in balls:
                    if ball.dragging:
                        ball.dragging = False
                        if last_mouse_pos:
                            dx = event.pos[0] - last_mouse_pos[0]
                            dy = event.pos[1] - last_mouse_pos[1]
                            ball.velocity = [dx / 5, dy / 5]
                        last_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION:
                for ball in balls:
                    if ball.dragging:
                        ball.rect.center = event.pos
                        if last_mouse_pos:
                            last_mouse_pos = event.pos

            # Sağ tıklama menüsü işlemleri
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if cat.rect.collidepoint(event.pos):
                    cat.show_menu = True
                else:
                    top_x = event.pos[0]
                    top_y = event.pos[1]
                    if not any(ball.rect.collidepoint(event.pos) for ball in balls):
                        new_ball = Ball(top_x, top_y)
                        balls.add(new_ball)
                        new_ball.velocity = [0, 0]
                        logger.info(f"Top oluşturuldu. Konum: ({top_x}, {top_y})")

            if cat.show_menu:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    cat.handle_menu_click(event.pos, house, CUSTOMIZATION_MENU)

        elif current_menu == CUSTOMIZATION_MENU:
            handle_customization_menu_event(event)

    # Objelerin durumunu güncelle
    cat.update(house,balls)
    balls.update()

    # Kedi topa doğru yürüyecek mi?
    if len(balls) > 0 and not cat.is_inside_house:
        nearest_ball = cat.find_nearest_ball(balls)
        if nearest_ball:
            cat_walking_to_ball = True
            cat.walk_to_target(nearest_ball.rect.centerx, nearest_ball.rect.centery)
            # Top yakalandı mı?
            distance = math.sqrt((cat.rect.centerx - nearest_ball.rect.centerx)**2 + (cat.rect.centery - nearest_ball.rect.centery)**2)
            if distance < 5:  # Yakalama mesafesini küçült (örneğin 5 piksel)
                balls.remove(nearest_ball)
                cat.walking_animation = False
        else:
            cat_walking_to_ball = False
    else:
        cat_walking_to_ball = False

    if cat.dragging:
        cat.show_menu = False

    # Ekranı temizle
    screen.fill((255, 255, 255))

    # Özelleştirme menüsünü çiz (eğer gösteriliyorsa)
    print(f"current_menu değeri (main.py, çizim öncesi): {current_menu}")  # Hata ayıklama için
    if current_menu == CUSTOMIZATION_MENU:
        print(f"current_menu değeri (main.py, çizim İÇİNDE): {current_menu}")  # Hata ayıklama için
        draw_customization_menu(screen)

    # Objeleri çiz
    balls.draw(screen)
    house.draw(screen)
    cat.draw(screen)

    # Kedinin menüsünü çiz (eğer gösteriliyorsa)
    if cat.show_menu and current_menu == MAIN_MENU:
        cat.draw_menu(screen, cat.rect.right, cat.rect.top)

    # Ekranı güncelle
    pygame.display.flip()

    # FPS
    clock.tick(60)

# Pygame'i sonlandır
pygame.quit()
logger.info("Oyun kapatıldı.")