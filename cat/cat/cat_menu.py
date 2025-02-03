import pygame

class CatMenu:
    def __init__(self, kedi):
        self.kedi = kedi
        self.menu_acik = False
        self.menu_rect = pygame.Rect(0, 0, 150, 100)
        self.buton_yuksekligi = 24
        self.buton_genisligi = self.buton_yuksekligi
        self.menu_butonlari = {}
        self.menu_yazilari = {}

    def ciz_menu(self, screen):
        # Butonları ve yazıları güncelle
        self.menu_butonlari = {
            "aclik": pygame.Rect(self.menu_rect.x - self.buton_genisligi - 5, self.menu_rect.y + 10, self.buton_genisligi, self.buton_yuksekligi),
            "mutluluk": pygame.Rect(self.menu_rect.x - self.buton_genisligi - 5, self.menu_rect.y + 35, self.buton_genisligi, self.buton_yuksekligi),
            "uyku": pygame.Rect(self.menu_rect.x - self.buton_genisligi - 5, self.menu_rect.y + 60, self.buton_genisligi, self.buton_yuksekligi),
        }
        self.menu_yazilari = {
            "aclik": f"Açlık: %{int(self.kedi.aclik)}",
            "mutluluk": f"Mutluluk: %{int(self.kedi.mutluluk)}",
            "uyku": f"Uyku: %{int(self.kedi.uyku)}",
        }

        # Menüyü çiz (opak beyaz arkaplan)
        pygame.draw.rect(screen, (255, 255, 255, 255), self.menu_rect)

        # Butonları çiz
        for buton in self.menu_butonlari.values():
            pygame.draw.rect(screen, (100, 100, 100), buton)

        # Değerleri yazdır
        font = pygame.font.Font(None, 24)
        y = 10
        for yazi in self.menu_yazilari.values():
            text_surface = font.render(yazi, True, (0, 0, 0))
            screen.blit(text_surface, (self.menu_rect.x + 10, self.menu_rect.y + y))
            y += 25

    def ac_kapa_menu(self, x, y, screen_width):
      self.menu_acik = not self.menu_acik
      if self.menu_acik:
        self.menu_rect.topleft = (x, y)
        if self.menu_rect.right > screen_width:
          self.menu_rect.topleft = (x - self.menu_rect.width - 5, y)