import pygame
import win32api
import win32con
import win32gui
import time
import random
from cat.cat import Kedi
from cat_house import KediEvi
from top import Top
import os

def log_message(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(os.path.join("log", "Logger.log"), "a") as log_file:
        log_file.write(log_entry + "\n")
        
def oyun_dongusu(screen, screen_width, screen_height, kedi, ev):
    clock = pygame.time.Clock()
    running = True
    dragging_kedi = False
    drag_offset_kedi = (0, 0)
    top = None
    top_alindi = False
    topun_konumu = None
    dragging_top = False
    drag_offset_ev = (0, 0)
    top_olusturma_zamani = None  # Topun oluşturulacağı zamanı tutacak değişken

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if kedi.rect.collidepoint(event.pos):
                        log_message("Kediye tıklandı.")
                        kedi.istatistikler.besle(dragging_kedi)
                        dragging_kedi = True
                        drag_offset_kedi = (kedi.x - event.pos[0], kedi.y - event.pos[1])
                        kedi.menu.menu_acik = False
                    elif ev.rect.collidepoint(event.pos):
                        log_message("Eve tıklandı.")
                        ev.dragging = True
                        drag_offset_kedi = (kedi.x - event.pos[0], kedi.y - event.pos[1])
                        drag_offset_ev = (ev.x - event.pos[0], ev.y - event.pos[1])
                    elif top and top.rect.collidepoint(event.pos):
                        log_message("Topa tıklandı.")
                        dragging_top = True
                        drag_offset_top = (top.x - event.pos[0], top.y - event.pos[1])
                elif event.button == 3:
                    if ev.rect.collidepoint(event.pos):
                        log_message("Eve sağ tıklandı.")
                        top_alindi = ev.handle_event(event, kedi, top_alindi)
                        if top_alindi:
                            top = Top(random.randint(0, screen_width - 25), random.randint(0, screen_height - 25), screen_width, screen_height)
                            topun_konumu = None
                            log_message("Top oluşturuldu.")
                    if kedi.rect.collidepoint(event.pos):
                        log_message("Kediye sağ tıklandı.")
                        kedi.handle_event(event) # Menu olaylarını işle
                if kedi.menu.menu_acik == True and not ev.rect.collidepoint(event.pos):
                    kedi.menu.menu_acik = False
                    top_alindi = False
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_kedi = False
                if ev.dragging:
                    ev.dragging = False
                    if not kedi.evin_icinde_mi(ev.rect):
                        hedef_x = ev.rect.centerx - kedi.rect.width / 2
                        hedef_y = ev.rect.centery - kedi.rect.height / 2
                        kedi.hareket.yurume_baslat((hedef_x, hedef_y))
                if ev.rect.collidepoint(event.pos): # Bu kontrol dışarı taşındı
                    if kedi.evin_icinde_mi(ev.rect):
                        kedi.istatistikler.uyu()
                if dragging_top:
                    dragging_top = False
                    top.rastgele_hareket_baslat()
                    log_message(f"Top bırakıldı. Konum: ({top.x}, {top.y})") # LOGLAMA EKLENDİ
            elif event.type == pygame.MOUSEMOTION:
                if dragging_kedi:
                    mouse_x, mouse_y = event.pos
                    kedi.x = mouse_x + drag_offset_kedi[0]
                    kedi.y = mouse_y + drag_offset_kedi[1]
                    kedi.x = max(0, min(kedi.x, screen_width - kedi.rect.width))
                    kedi.y = max(0, min(kedi.y, screen_height - kedi.rect.height))
                    kedi.rect.topleft = (kedi.x, kedi.y)
                    log_message(f"Kedi konumu güncellendi: ({kedi.x}, {kedi.y})") # LOGLAMA EKLENDİ
                elif ev.dragging and not dragging_kedi:
                    mouse_x, mouse_y = event.pos
                    ev.x = mouse_x + drag_offset_ev[0]
                    ev.y = mouse_y + drag_offset_ev[1]
                    ev.x = max(0, min(ev.x, screen_width - ev.rect.width))
                    ev.y = max(0, min(ev.y, screen_height - ev.rect.height))
                    ev.rect.topleft = (ev.x, ev.y)
                    ev.hareket_ettir(kedi)
                elif dragging_top:
                    mouse_x, mouse_y = event.pos
                    top.x = mouse_x + drag_offset_top[0]
                    top.y = mouse_y + drag_offset_top[1]
                    top.rect.topleft = (top.x, top.y)
                    log_message(f"Top konumu güncellendi: ({top.x}, {top.y})")  # LOGLAMA EKLENDİ
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    kedi.durum = "yuruyor"
                    kedi.hareket.hareket_baslangic_zamani = kedi.istatistikler.besleme_zamanı
                    kedi.animasyonlar.resim_degistirme_zamani = kedi.istatistikler.besleme_zamanı

        # Ekranı temizle (saydam renkle doldur)
        screen.fill((0, 0, 0, 0))

        # Ev ve kediyi çiz
        ev.ciz(screen)
        kedi.ciz(screen)

        # Topu çiz ve hareket ettir
        if top:
            if not dragging_top:
                top.hareket_ettir()
            top.ciz(screen)
            if top.hareket_basladi:
                kedi.durum = "topu_takip_et"
                kedi.hareket.yurume_baslat((top.x, top.y))
                kedi.hareket.yuru()
            else:
                if kedi.durum == "topu_takip_et":
                    kedi.durum = "normal"
                    kedi.animasyonlar.resim_index = 0
                    kedi.animasyonlar.guncel_resim = kedi.animasyonlar.oturma_resimleri[kedi.animasyonlar.resim_index]
                    kedi.animasyonlar.resim_degistirme_zamani = kedi.istatistikler.besleme_zamanı
                    kedi.rect = kedi.animasyonlar.guncel_resim.get_rect(topleft=(kedi.x, kedi.y))

        # Kedinin durumunu güncelle
        kedi.guncelle()

        # Ekranı güncelle
        pygame.display.flip()

        # FPS'yi ayarla
        clock.tick(60)