import pygame
import os

import pygame
import os

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(os.path.join("log", "Logger.log"), "a") as log_file:
        log_file.write(log_entry + "\n")

class CatAnimations:
    def __init__(self, kedi):
        self.kedi = kedi
        self.oturma_resimleri = []
        for resim in ["oturma.png", "oturma2.png"]:
            img = pygame.image.load(os.path.join(self.kedi.PIC_FOLDER, resim)).convert_alpha()  # Değişiklik burada
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w // 4, h // 4))
            self.oturma_resimleri.append(img)
        self.yurume_resimleri_sag = []
        for resim in ["yurume.png", "yurume2.png"]:
            img = pygame.image.load(os.path.join(self.kedi.PIC_FOLDER, resim)).convert_alpha()  # Değişiklik burada
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w // 4, h // 4))
            self.yurume_resimleri_sag.append(img)
        self.yurume_resimleri_sol = []
        for resim in ["yurume_sol.png", "yurume_sol2.png"]:
            img = pygame.image.load(os.path.join(self.kedi.PIC_FOLDER, resim)).convert_alpha()  # Değişiklik burada
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w // 4, h // 4))
            self.yurume_resimleri_sol.append(img)
        self.guncel_resim = self.oturma_resimleri[0]
        self.resim_degistirme_zamani = self.kedi.besleme_zamanı
        self.resim_index = 0

    def animasyonu_guncelle(self):
        simdi = self.kedi.besleme_zamanı
        if self.kedi.durum == "normal" or self.kedi.durum == "yiyor" or self.kedi.durum == "uyuyor":
            # Oturma animasyonu
            if simdi - self.resim_degistirme_zamani > 60:
                self.resim_index = (self.resim_index + 1) % len(self.kedi.oturma_resimleri)
                self.guncel_resim = self.kedi.oturma_resimleri[self.resim_index]
                self.resim_degistirme_zamani = simdi
                self.kedi.rect = self.guncel_resim.get_rect(topleft=(self.kedi.x, self.kedi.y))
            if self.kedi.durum == "yiyor":
                self.kedi.durum = "normal"
        elif self.kedi.durum == "yuruyor" or self.kedi.durum == "eve_yuruyor":
            # Yürüme animasyonu
            if simdi - self.resim_degistirme_zamani > 0.3:
                self.resim_index = (self.resim_index + 1) % len(self.kedi.yurume_resimleri_sag)
                if self.kedi.yurume_yonu == 1:
                    self.guncel_resim = self.kedi.yurume_resimleri_sag[self.resim_index]
                else:
                    self.guncel_resim = self.kedi.yurume_resimleri_sol[self.resim_index]
                self.resim_degistirme_zamani = simdi
                self.kedi.rect = self.guncel_resim.get_rect(topleft=(self.kedi.x, self.kedi.y))