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

# Menü durumları
MAIN_MENU = 0
CUSTOMIZATION_MENU = 1

# Renk seçenekleri
cat_colors = {
    "Sarı": (255, 255, 0),
    "Siyah": (0, 0, 0),
    "Beyaz": (255, 255, 255),
    "Gri": (128, 128, 128)
}

class Game:
    def __init__(self):
        self.cat = Cat(100, 400)
        self.house = House(500, 350)
        self.balls = pygame.sprite.Group()
        ball = Ball(150, 30)
        self.balls.add(ball)
        self.current_menu = MAIN_MENU
        self.selected_color = "Sarı"  # Varsayılan renk
        self.cat_name = "Minnoş"  # Kedinin adını saklamak için değişken
        self.profile_tab_active = False  # Profil sekmesinin açık olup olmadığını takip eden değişken
        self.editing_name = False # İsim düzenleme
        self.name_input_rect = None # Bunu daha sonra tanımlayacağız

    def draw_customization_menu(self, screen):
        """Özelleştirme menüsünü çizer."""
        menu_width = 500  # Menü genişliğini artır
        menu_height = 400  # Menü yüksekliğini artır
        menu_x = screen_width // 2 - menu_width // 2
        menu_y = screen_height // 2 - menu_height // 2

        # Menü arkaplanı
        pygame.draw.rect(screen, (200, 200, 200), (menu_x, menu_y, menu_width, menu_height))

        font = pygame.font.Font(None, 30)

        # Başlık (Artık menü çubuğunda olacak)
        # title_text = font.render("Özelleştirme", True, (0, 0, 0))
        # title_rect = title_text.get_rect(center=(screen_width // 2, menu_y + 30))
        # screen.blit(title_text, title_rect)

        # Menü çubuğu (sidebar)
        sidebar_width = 150
        pygame.draw.rect(screen, (150, 150, 150), (menu_x, menu_y, sidebar_width, menu_height))

        # Profil sekmesi butonu
        profile_button_rect = pygame.Rect(menu_x, menu_y, sidebar_width, 50)  # Biraz boşluk bırak
        if self.profile_tab_active:
             pygame.draw.rect(screen,(170, 170, 170), profile_button_rect) # Aktif sekme için biraz daha koyu renk
        profile_text = font.render("Profil", True, (0, 0, 0))
        profile_text_rect = profile_text.get_rect(center=profile_button_rect.center)
        screen.blit(profile_text, profile_text_rect)
        # Diğer sekmeler buraya eklenebilir (Örn: Renk, Desen, Aksesuar...)

        # İçerik alanı (Sağ taraf)
        content_x = menu_x + sidebar_width
        content_width = menu_width - sidebar_width
        content_rect = pygame.Rect(content_x, menu_y, content_width, menu_height)

        if self.profile_tab_active:
            self.draw_profile_tab(screen, content_rect)  # Profil sekmesi içeriğini çiz

        # Geri butonu (Menü çubuğunun altında)
        back_button_rect = pygame.Rect(menu_x, menu_y + menu_height - 50, sidebar_width, 40)
        pygame.draw.rect(screen, (100, 100, 100), back_button_rect)
        back_text = font.render("Geri", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

    def draw_profile_tab(self, screen, rect):
        """Profil sekmesi içeriğini çizer."""
        font = pygame.font.Font(None, 25)

        # Kedi görseli (basit bir kare şimdilik)
        cat_image_rect = pygame.Rect(rect.x + 20, rect.y + 20, 100, 100)
        pygame.draw.rect(screen, self.selected_color, cat_image_rect)
        # TODO: Gerçek kedi görselini çiz

        # Kedi adı
        name_label_text = font.render("İsim:", True, (0, 0, 0))
        name_label_rect = name_label_text.get_rect(topleft=(cat_image_rect.right + 20, rect.y + 20))
        screen.blit(name_label_text, name_label_rect)

        # İsim kutusu
        name_text = font.render(self.cat_name, True, (0,0,0))
        name_rect = name_text.get_rect(topleft=(name_label_rect.right + 10 , rect.y + 15))
        
        
        if self.editing_name:
          self.name_input_rect = pygame.Rect(name_rect.left -5 , name_rect.top - 5, 170, name_rect.height + 10) # name_input_rect'i tanımla
          pygame.draw.rect(screen, (255, 255, 255), self.name_input_rect)
          pygame.draw.rect(screen, (0,0,0), self.name_input_rect, 2) # Siyah Çerçeve
        else:
          self.name_input_rect = None # Eğer düzenlemede değilsek None yap

        screen.blit(name_text, name_rect)

    def handle_customization_menu_event(self, event):
        """Özelleştirme menüsündeki olayları işler."""
        menu_width = 300
        menu_height = 300  # Menü yüksekliğini artır
        menu_x = screen_width // 2 - menu_width // 2
        menu_y = screen_height // 2 - menu_height // 2
        sidebar_width = 150

        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
              # Profil sekmesi butonu
              profile_button_rect = pygame.Rect(menu_x, menu_y, sidebar_width, 50)
              if profile_button_rect.collidepoint(event.pos):
                  self.profile_tab_active = True
                  return  # Başka bir şey yapmadan fonksiyondan çık

              # Geri butonu
              back_button_rect = pygame.Rect(menu_x, menu_y + menu_height - 50, sidebar_width, 40)
              if back_button_rect.collidepoint(event.pos):
                  self.current_menu = MAIN_MENU
                  print("Ana menüye dönüldü.")
                  return  # Başka bir şey yapmadan fonksiyondan çık
              
              # İsim düzenleme
              if self.profile_tab_active and self.name_input_rect and self.name_input_rect.collidepoint(event.pos):
                self.editing_name = True
              else:
                self.editing_name = False
        elif event.type == pygame.KEYDOWN and self.editing_name:  # İsim düzenleme kısmı
            if event.key == pygame.K_RETURN:
                self.editing_name = False
            elif event.key == pygame.K_BACKSPACE:
                self.cat_name = self.cat_name[:-1]
            else:
                # Karakter sınırı koy
                if len(self.cat_name) < 15:  #  karakter sınırı (örnek olarak 15)
                    self.cat_name += event.unicode

    def switch_to_customization_menu(self):
      """Özelleştirme menüsüne geçiş yapar."""
      self.current_menu = CUSTOMIZATION_MENU
      logger.info("Özelleştirme menüsüne geçildi.")

    def run(self):
        running = True
        last_mouse_pos = None
        cat_walking_to_ball = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.current_menu == MAIN_MENU:
                    # Kedi olayları işleme
                    if self.cat.handle_event(event):
                        continue

                    # Ev olayları işleme
                    if self.house.handle_event(event, self.balls, self.cat):
                        continue

                    # Top olayları işleme
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for ball in self.balls:
                            if ball.rect.collidepoint(event.pos):
                                ball.dragging = True
                                ball.velocity = [0, 0]
                                last_mouse_pos = event.pos
                                break
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        for ball in self.balls:
                            if ball.dragging:
                                ball.dragging = False
                                if last_mouse_pos:
                                    dx = event.pos[0] - last_mouse_pos[0]
                                    dy = event.pos[1] - last_mouse_pos[1]
                                    ball.velocity = [dx / 5, dy / 5]
                                last_mouse_pos = None
                    elif event.type == pygame.MOUSEMOTION:
                        for ball in self.balls:
                            if ball.dragging:
                                ball.rect.center = event.pos
                                if last_mouse_pos:
                                    last_mouse_pos = event.pos

                    # Sağ tıklama menüsü işlemleri
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        if self.cat.rect.collidepoint(event.pos):
                            self.cat.show_menu = True
                        else:
                            top_x = event.pos[0]
                            top_y = event.pos[1]
                            if not any(ball.rect.collidepoint(event.pos) for ball in self.balls):
                                new_ball = Ball(top_x, top_y)
                                self.balls.add(new_ball)
                                new_ball.velocity = [0, 0]
                                logger.info(f"Top oluşturuldu. Konum: ({top_x}, {top_y})")

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.cat.show_menu:
                            self.cat.handle_menu_click(event.pos, self.house, self)

                elif self.current_menu == CUSTOMIZATION_MENU:
                    self.handle_customization_menu_event(event)

            # Objelerin durumunu güncelle
            self.cat.update(self.house, self.balls)
            self.balls.update()

            if len(self.balls) > 0 and not self.cat.is_inside_house:
                nearest_ball = self.cat.find_nearest_ball(self.balls)
                if nearest_ball:
                    cat_walking_to_ball = True
                    self.cat.walk_to_target(nearest_ball.rect.centerx, nearest_ball.rect.centery)
                    if self.cat.rect.colliderect(nearest_ball.rect):
                        self.balls.remove(nearest_ball)
                        self.cat.walking_animation = False
                        cat_walking_to_ball = False
                else:
                    cat_walking_to_ball = False

            if self.cat.dragging:
                self.cat.show_menu = False

            # Ekranı temizle
            screen.fill((255, 255, 255))

            # Objeleri çiz
            self.balls.draw(screen)
            self.house.draw(screen)
            self.cat.draw(screen)

            # Kedinin menüsünü çiz (eğer gösteriliyorsa ve ana menüdeysek)
            if self.cat.show_menu and self.current_menu == MAIN_MENU:
                self.cat.draw_menu(screen, self.cat.rect.right, self.cat.rect.top)

            # Özelleştirme menüsünü çiz (eğer gösteriliyorsa)
            if self.current_menu == CUSTOMIZATION_MENU:
                self.draw_customization_menu(screen)

            # Ekranı güncelle
            pygame.display.flip()

            # FPS
            clock.tick(60)

        # Pygame'i sonlandır
        pygame.quit()
        logger.info("Oyun kapatıldı.")

if __name__ == "__main__":
    game = Game()
    game.run()