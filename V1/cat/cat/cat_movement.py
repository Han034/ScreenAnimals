import time
import os
def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(os.path.join("log", "Logger.log"), "a") as log_file:
        log_file.write(log_entry + "\n")
class CatMovement:
    def __init__(self, kedi):
        self.kedi = kedi

    def hareket_et(self, dx, dy):
        if self.kedi.durum == "normal" or self.kedi.durum == "yuruyor" or self.kedi.durum == "eve_yuruyor":
            yeni_x = self.kedi.x + dx
            yeni_y = self.kedi.y + dy
            yeni_x = max(0, min(yeni_x, self.kedi.screen_width - self.kedi.rect.width))
            yeni_y = max(0, min(yeni_y, self.kedi.screen_height - self.kedi.rect.height))
            # Sadece kedi hareket ettiğinde menüyü kapat
            if dx != 0 or dy != 0:
                self.kedi.menu.menu_acik = False
            self.kedi.x = yeni_x
            self.kedi.y = yeni_y
            self.kedi.rect.topleft = (self.kedi.x, self.kedi.y)

    def yurume_baslat(self, hedef_konum):
        self.kedi.hedef_konum = hedef_konum
        self.kedi.durum = "eve_yuruyor"
        self.kedi.hareket_baslangic_zamani = self.kedi.besleme_zamanı
        self.kedi.resim_degistirme_zamani = self.kedi.besleme_zamanı

    def yuru(self):
        if self.kedi.durum == "eve_yuruyor" and self.kedi.hedef_konum:
            hedef_x, hedef_y = self.kedi.hedef_konum

            # X ekseninde yürüme
            if self.kedi.x < hedef_x - 2:
                self.hareket_et(2, 0)
                self.kedi.yurume_yonu = 1
            elif self.kedi.x > hedef_x + 2:
                self.hareket_et(-2, 0)
                self.kedi.yurume_yonu = -1
            else:
                # Y ekseninde yürüme
                if self.kedi.y < hedef_y - 2:
                    self.hareket_et(0, 2)
                elif self.kedi.y > hedef_y + 2:
                    self.hareket_et(0, -2)

            # Hedefe varınca durumu güncelle ve animasyon değiştir
            if abs(self.kedi.x - hedef_x) < 5 and abs(self.kedi.y - hedef_y) < 5:
                self.kedi.durum = "normal"
                self.kedi.hedef_konum = None
                self.kedi.animasyonlar.resim_index = 0
                self.kedi.animasyonlar.guncel_resim = self.kedi.animasyonlar.oturma_resimleri[self.kedi.animasyonlar.resim_index]
                self.kedi.animasyonlar.resim_degistirme_zamani = self.kedi.besleme_zamanı
                self.kedi.rect = self.kedi.animasyonlar.guncel_resim.get_rect(topleft=(self.kedi.x, self.kedi.y))