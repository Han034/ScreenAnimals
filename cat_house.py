import pygame
import os

class KediEvi:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dragging = False
        self.drag_offset = (0, 0)
        self.PIC_FOLDER = os.path.join(os.path.dirname(__file__), "pic")
        img = pygame.image.load(os.path.join(self.PIC_FOLDER, "ev.png")).convert_alpha()
        w, h = img.get_size()
        self.image = pygame.transform.scale(img, (w // 4, h // 4))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.menu_acik = False
        self.menu_rect = pygame.Rect(0, 0, 100, 50)
        self.menu_butonlari = {
            "top_al": pygame.Rect(0, 0, 80, 25),
        }

    def ciz(self, screen):
        screen.blit(self.image, self.rect)
        if self.menu_acik:
            self.ciz_menu(screen)

    def handle_event(self, event, kedi, top_alindi):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and self.rect.collidepoint(event.pos):
                self.menu_acik = not self.menu_acik
                if self.menu_acik:
                    self.menu_rect.topleft = (self.rect.right + 5, self.rect.top)
                    if self.menu_rect.right > self.screen_width:
                        self.menu_rect.topleft = (
                            self.rect.left - self.menu_rect.width - 5,
                            self.rect.top,
                        )
                    # Buton konumlarını güncelle
                    self.menu_butonlari["top_al"].topleft = (
                        self.menu_rect.x + 10,
                        self.menu_rect.y + 10,
                    )

            elif self.menu_acik:
                if event.button == 1:
                    for buton_adi, buton_rect in self.menu_butonlari.items():
                        if buton_rect.collidepoint(event.pos):
                            if buton_adi == "top_al":
                                return True  # Top alma butonuna tıklandığını belirt

                if not self.menu_rect.collidepoint(event.pos):
                    self.menu_acik = False

            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset = (self.x - event.pos[0], self.y - event.pos[1])

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                if not kedi.evin_icinde_mi(self.rect):
                    hedef_x = self.rect.centerx - kedi.rect.width / 2
                    hedef_y = self.rect.centery - kedi.rect.height / 2
                    kedi.hareket.yurume_baslat((hedef_x, hedef_y))
            # Bu kısmı MOUSEBUTTONDOWN'dan taşıdık
            if self.rect.collidepoint(event.pos):
                if kedi.evin_icinde_mi(self.rect):
                    kedi.istatistikler.uyu()

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.x = mouse_x + self.drag_offset[0]
                self.y = mouse_y + self.drag_offset[1]
                self.x = max(0, min(self.x, self.screen_width - self.rect.width))
                self.y = max(0, min(self.y, self.screen_height - self.rect.height))
                self.rect.topleft = (self.x, self.y)
        return False
    def ciz_menu(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.menu_rect)
        for buton_adi, buton_rect in self.menu_butonlari.items():
            pygame.draw.rect(screen, (100, 100, 100), buton_rect)
            font = pygame.font.Font(None, 20)
            text_surface = font.render(buton_adi.replace("_", " ").title(), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=buton_rect.center)
            screen.blit(text_surface, text_rect)