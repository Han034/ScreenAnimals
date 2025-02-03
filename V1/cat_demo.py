import pygame
import time
import os

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(os.path.join("log", "Logger.log"), "a") as log_file:
        log_file.write(log_entry + "\n")

class Kedi:
    def __init__(self, x, y, screen_width, screen_height, ev):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.aclik = 100.0
        self.mutluluk = 100.0
        self.uyku = 0.0
        self.besleme_zamanı = time.time()
        self.uyku_baslangic_zamani = time.time()
        self.mutluluk_zamanı = time.time()
        self.durum = "normal"
        self.PIC_FOLDER = os.path.join(os.path.dirname(__file__), "pic")
        self.oturma_resimleri = []
        for resim in ["oturma.png", "oturma2.png"]:
            img = pygame.image.load(os.path.join(self.PIC_FOLDER, resim)).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w // 4, h // 4))
            self.oturma_resimleri.append(img)
        self.yurume_resimleri_sag = []
        for resim in ["yurume.png", "yurume2.png"]:
            img = pygame.image.load(os.path.join(self.PIC_FOLDER, resim)).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w // 4, h // 4))
            self.yurume_resimleri_sag.append(img)
        self.yurume_resimleri_sol = []
        for resim in ["yurume_sol.png", "yurume_sol2.png"]:
            img = pygame.image.load(os.path.join(self.PIC_FOLDER, resim)).convert_alpha()
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w // 4, h // 4))
            self.yurume_resimleri_sol.append(img)
        self.guncel_resim = self.oturma_resimleri[0]
        self.resim_degistirme_zamani = time.time()
        self.resim_index = 0
        self.hareket_baslangic_zamani = time.time()
        self.yurume_yonu = 1
        self.rect = self.guncel_resim.get_rect(topleft=(x, y))
        self.menu_acik = False
        self.menu_rect = pygame.Rect(0, 0, 150, 100)
        self.hedef_konum = None
        self.buton_yuksekligi = 24  # Buton yüksekliği, yazı yüksekliği ile aynı
        self.buton_genisligi = self.buton_yuksekligi
        self.menu_butonlari = {} # Boş sözlük
        self.menu_yazilari = {}
        self.ev = ev  # Ev objesini kaydet

    def ciz(self, screen):
        screen.blit(self.guncel_resim, self.rect)
        if self.menu_acik:
            self.ciz_menu(screen)

    def besle(self, dragging_kedi):
        if not dragging_kedi:
            self.aclik = min(100.0, self.aclik + 20)
            self.besleme_zamanı = time.time()
            self.durum = "yiyor"

    def uyu(self):
        if self.durum != "uyuyor":
            self.durum = "uyuyor"
            self.uyku_baslangic_zamani = time.time()
            self.uyku = 0.0

    def guncelle(self):
        simdi = time.time()
        zaman_gecisi = simdi - self.besleme_zamanı
        self.aclik = max(0.0, self.aclik - (80.0 / 600.0) * zaman_gecisi)
        self.besleme_zamanı = simdi

        mutluluk_zaman_gecisi = simdi - self.mutluluk_zamanı
        if self.aclik > 50.0 and self.uyku < 50.0:
            self.mutluluk = min(100.0, self.mutluluk + (50.0 / (10.0 * 60.0)) * mutluluk_zaman_gecisi)
        elif self.aclik < 20.0 or self.uyku > 80.0:
            self.mutluluk = max(0.0, self.mutluluk - (50.0 / (10.0 * 60.0)) * mutluluk_zaman_gecisi)
        self.mutluluk_zamanı = simdi

        if self.durum == "uyuyor":
            uyku_zaman_gecisi = simdi - self.uyku_baslangic_zamani
            self.uyku = max(0.0, self.uyku - (80.0 / (20.0 * 60.0)) * uyku_zaman_gecisi)
            if self.uyku < 0.01:
              self.uyku = 0.0
              self.durum = "normal"
        else:
            if self.aclik < 15.0 or self.uyku < 10.0:
                self.uyku = min(100.0, self.uyku + (80.0 / (20.0 * 60.0)) * zaman_gecisi)

        if self.aclik < 0.01:
            self.aclik = 0.0
            self.durum = "kaciyor"
        if self.mutluluk < 0.01:
            self.mutluluk = 0.0
            self.durum = "kaciyor"

        self.animasyonu_guncelle()
        if self.durum == "eve_yuruyor":
          self.yuru()

    def hareket_et(self, dx, dy):
        if self.durum == "normal" or self.durum == "yuruyor" or self.durum == "eve_yuruyor":
            yeni_x = self.x + dx
            yeni_y = self.y + dy
            yeni_x = max(0, min(yeni_x, self.screen_width - self.rect.width))
            yeni_y = max(0, min(yeni_y, self.screen_height - self.rect.height))
            self.x = yeni_x
            self.y = yeni_y
            self.rect.topleft = (self.x, self.y)
            self.menu_acik = False  # Kedinin menüsünü kapat

    def evin_icinde_mi(self, ev_rect):
        return ev_rect.colliderect(self.rect)

    def animasyonu_guncelle(self):
        simdi = time.time()
        if self.durum == "normal" or self.durum == "yiyor" or self.durum == "uyuyor":
            # Oturma animasyonu
            if simdi - self.resim_degistirme_zamani > 60:
                self.resim_index = (self.resim_index + 1) % len(self.oturma_resimleri)
                self.guncel_resim = self.oturma_resimleri[self.resim_index]
                self.resim_degistirme_zamani = simdi
                self.rect = self.guncel_resim.get_rect(topleft=(self.x, self.y))
            if self.durum == "yiyor":
                self.durum = "normal"
        elif self.durum == "yuruyor" or self.durum == "eve_yuruyor":
            # Yürüme animasyonu
            if simdi - self.resim_degistirme_zamani > 0.3:
                self.resim_index = (self.resim_index + 1) % len(self.yurume_resimleri_sag)
                if self.yurume_yonu == 1:
                  self.guncel_resim = self.yurume_resimleri_sag[self.resim_index]
                else:
                  self.guncel_resim = self.yurume_resimleri_sol[self.resim_index]
                self.resim_degistirme_zamani = simdi
                self.rect = self.guncel_resim.get_rect(topleft=(self.x, self.y))

    def ciz_menu(self, screen):
        # Butonları ve yazıları güncelle
        self.menu_butonlari = {
            "aclik": pygame.Rect(self.menu_rect.x - self.buton_genisligi - 5, self.menu_rect.y + 10, self.buton_genisligi, self.buton_yuksekligi),
            "mutluluk": pygame.Rect(self.menu_rect.x - self.buton_genisligi - 5, self.menu_rect.y + 35, self.buton_genisligi, self.buton_yuksekligi),
            "uyku": pygame.Rect(self.menu_rect.x - self.buton_genisligi - 5, self.menu_rect.y + 60, self.buton_genisligi, self.buton_yuksekligi),
        }
        self.menu_yazilari = {
            "aclik": f"Açlık: %{int(self.aclik)}",
            "mutluluk": f"Mutluluk: %{int(self.mutluluk)}",
            "uyku": f"Uyku: %{int(self.uyku)}",
        }
        
        # Menüyü çiz
        pygame.draw.rect(screen, (255, 255, 255), self.menu_rect)

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and self.rect.collidepoint(event.pos):
                self.menu_acik = not self.menu_acik
                if self.menu_acik:
                    self.menu_rect.topleft = (self.rect.right + 5, self.rect.top)
                    if self.menu_rect.right > self.screen_width:
                        self.menu_rect.topleft = (self.rect.left - self.menu_rect.width - 5, self.rect.top)
            elif self.menu_acik:
                if event.button == 1:  # Sol tıklama kontrolü eklendi
                    for buton_adi, buton_rect in self.menu_butonlari.items():
                        if buton_rect.collidepoint(event.pos):
                            if buton_adi == "aclik":
                                self.besle(False)
                            elif buton_adi == "mutluluk":
                                print("Mutluluk Butonu Tıklandı")
                            elif buton_adi == "uyku":
                                self.durum = "eve_yuruyor"
                                hedef_x = self.ev.rect.centerx - self.rect.width / 2  # Ev bilgisini kullanarak hedef konum hesaplanıyor
                                hedef_y = self.ev.rect.centery - self.rect.height / 2
                                self.yurume_baslat((hedef_x, hedef_y))
                if not self.menu_rect.collidepoint(event.pos):
                    self.menu_acik = False

    def yurume_baslat(self, hedef_konum):
        self.hedef_konum = hedef_konum
        self.durum = "eve_yuruyor"
        self.hareket_baslangic_zamani = time.time()
        self.resim_degistirme_zamani = time.time()

    def yuru(self):
        if self.durum == "eve_yuruyor" and self.hedef_konum:
            hedef_x, hedef_y = self.hedef_konum

            # X ekseninde yürüme
            if self.x < hedef_x - 2:
                self.hareket_et(2, 0)
                self.yurume_yonu = 1
            elif self.x > hedef_x + 2:
                self.hareket_et(-2, 0)
                self.yurume_yonu = -1
            else:
                # Y ekseninde yürüme
                if self.y < hedef_y - 2:
                    self.hareket_et(0, 2)
                elif self.y > hedef_y + 2:
                    self.hareket_et(0, -2)

            # Hedefe varınca durumu güncelle ve animasyon değiştir
            if abs(self.x - hedef_x) < 5 and abs(self.y - hedef_y) < 5:
                self.durum = "normal"
                self.hedef_konum = None
                self.guncel_resim = self.oturma_resimleri[self.resim_index]
                self.resim_degistirme_zamani = time.time()
                self.rect = self.guncel_resim.get_rect(topleft=(self.x, self.y))