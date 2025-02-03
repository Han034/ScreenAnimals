import pygame
import time
import os
from .cat_animations import CatAnimations
from .cat_movement import CatMovement
from .cat_stats import CatStats
from .cat_menu import CatMenu

class Kedi:
    def __init__(self, x, y, screen_width, screen_height, ev):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ev = ev
        self.aclik = 100.0
        self.mutluluk = 100.0
        self.uyku = 0.0
        self.besleme_zamanı = time.time()
        self.uyku_baslangic_zamani = time.time()
        self.mutluluk_zamanı = time.time()
        self.durum = "normal"
        self.PIC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "pic") # Bir üst dizine çıkıp oradan pic klasörüne iniyoruz
        self.yurume_yonu = 1
        self.rect = pygame.Rect(x, y, 50, 50)  # Geçici boyut
        self.hedef_konum = None

        # Diğer sınıfları oluştur
        self.animasyonlar = CatAnimations(self)
        self.hareket = CatMovement(self)
        self.istatistikler = CatStats(self)
        self.menu = CatMenu(self)

    def ciz(self, screen):
        screen.blit(self.animasyonlar.guncel_resim, self.rect)
        if self.menu.menu_acik:
            self.menu.ciz_menu(screen)

    def guncelle(self):
        self.istatistikler.guncelle()
        self.animasyonlar.animasyonu_guncelle()
        if self.durum == "eve_yuruyor":
            self.hareket.yuru()

    def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 3 and self.rect.collidepoint(event.pos):
            self.menu.ac_kapa_menu(self.rect.right + 5, self.rect.top, self.screen_width)
          elif self.menu.menu_acik:
            if event.button == 1:
              for buton_adi, buton_rect in self.menu.menu_butonlari.items():
                if buton_rect.collidepoint(event.pos):
                  if buton_adi == "aclik":
                    self.istatistikler.besle(False)
                  elif buton_adi == "mutluluk":
                    print("Mutluluk Butonu Tıklandı")
                  elif buton_adi == "uyku":
                    self.durum = "eve_yuruyor"
                    hedef_x = self.ev.rect.centerx - self.rect.width / 2
                    hedef_y = self.ev.rect.centery - self.rect.height / 2
                    self.hareket.yurume_baslat((hedef_x, hedef_y))
              if not self.menu.menu_rect.collidepoint(event.pos):
                self.menu.menu_acik = False

    def evin_icinde_mi(self, ev_rect):
      return ev_rect.colliderect(self.rect)