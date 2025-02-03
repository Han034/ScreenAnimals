import time

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(os.path.join("log", "Logger.log"), "a") as log_file:
        log_file.write(log_entry + "\n")
class CatStats:
    def __init__(self, kedi):
        self.kedi = kedi

    def besle(self, dragging_kedi):
        if not dragging_kedi:
            self.kedi.aclik = min(100.0, self.kedi.aclik + 20)
            self.kedi.besleme_zamanı = time.time()
            self.kedi.durum = "yiyor"

    def uyu(self):
        if self.kedi.durum != "uyuyor":
            self.kedi.durum = "uyuyor"
            self.kedi.uyku_baslangic_zamani = time.time()
            self.kedi.uyku = 0.0

    def guncelle(self):
        simdi = time.time()
        zaman_gecisi = simdi - self.kedi.besleme_zamanı
        self.kedi.aclik = max(0.0, self.kedi.aclik - (80.0 / 600.0) * zaman_gecisi)
        self.kedi.besleme_zamanı = simdi

        mutluluk_zaman_gecisi = simdi - self.kedi.mutluluk_zamanı
        if self.kedi.aclik > 50.0 and self.kedi.uyku < 50.0:
            self.kedi.mutluluk = min(100.0, self.kedi.mutluluk + (50.0 / (10.0 * 60.0)) * mutluluk_zaman_gecisi)
        elif self.kedi.aclik < 20.0 or self.kedi.uyku > 80.0:
            self.kedi.mutluluk = max(0.0, self.kedi.mutluluk - (50.0 / (10.0 * 60.0)) * mutluluk_zaman_gecisi)
        self.kedi.mutluluk_zamanı = simdi

        if self.kedi.durum == "uyuyor":
            uyku_zaman_gecisi = simdi - self.kedi.uyku_baslangic_zamani
            self.kedi.uyku = max(0.0, self.kedi.uyku - (80.0 / (20.0 * 60.0)) * uyku_zaman_gecisi)
            if self.kedi.uyku < 0.01:
              self.kedi.uyku = 0.0
              self.kedi.durum = "normal"
        else:
            if self.kedi.aclik < 15.0 or self.kedi.uyku < 10.0:
                self.kedi.uyku = min(100.0, self.kedi.uyku + (80.0 / (20.0 * 60.0)) * zaman_gecisi)

        if self.kedi.aclik < 0.01:
            self.kedi.aclik = 0.0
            self.kedi.durum = "kaciyor"
        if self.kedi.mutluluk < 0.01:
            self.kedi.mutluluk = 0.0
            self.kedi.durum = "kaciyor"