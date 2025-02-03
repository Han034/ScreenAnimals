import pygame
import win32api
import win32con
import win32gui
import time
from cat.cat import Kedi
from cat_house import KediEvi
from top import Top

def oyun_dongusu(screen, screen_width, screen_height, kedi, ev):
    clock = pygame.time.Clock()
    running = True
    dragging_kedi = False
    drag_offset_kedi = (0, 0)
    top = None
    top_alindi = False
    topun_konumu = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if kedi.rect.collidepoint(event.pos):
                        kedi.istatistikler.besle(dragging_kedi)
                        dragging_kedi = True
                        drag_offset_kedi = (kedi.x - event.pos[0], kedi.y - event.pos[1])
                        kedi.menu.menu_acik = False
                    elif ev.rect.collidepoint(event.pos):
                        ev.dragging = True
                        drag_offset_kedi = (kedi.x - event.pos[0], kedi.y - event.pos[1])
                        drag_offset_ev = (ev.x - event.pos[0], ev.y - event.pos[1])
                    elif top_alindi:
                        # Topu bırakma işlemi
                        top = Top(event.pos[0], event.pos[1], screen_width, screen_height)
                        top.rastgele_hareket_baslat()
                        top_alindi = False
                        topun_konumu = None  # Top bırakıldığı için konumu sıfırla
                elif event.button == 3:
                    if ev.rect.collidepoint(event.pos):
                        if ev.handle_event(event, kedi, top_alindi):
                            top_alindi = True
                            topun_konumu = ev.rect.centerx, ev.rect.centery  # Topun konumunu evin merkezi olarak ayarla
                kedi.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_kedi = False
                if ev.dragging:
                    ev.dragging = False
                    if not kedi.evin_icinde_mi(ev.rect):
                        hedef_x = ev.rect.centerx - kedi.rect.width / 2
                        hedef_y = ev.rect.centery - kedi.rect.height / 2
                        kedi.hareket.yurume_baslat((hedef_x, hedef_y))
                    if ev.rect.collidepoint(event.pos):
                        if kedi.evin_icinde_mi(ev.rect):
                            kedi.istatistikler.uyu()
            elif event.type == pygame.MOUSEMOTION:
                if dragging_kedi:
                    mouse_x, mouse_y = event.pos
                    kedi.x = mouse_x + drag_offset_kedi[0]
                    kedi.y = mouse_y + drag_offset_kedi[1]
                    kedi.x = max(0, min(kedi.x, screen_width - kedi.rect.width))
                    kedi.y = max(0, min(kedi.y, screen_height - kedi.rect.height))
                    kedi.rect.topleft = (kedi.x, kedi.y)
                elif ev.dragging and not dragging_kedi:
                    mouse_x, mouse_y = event.pos
                    ev.x = mouse_x + drag_offset_ev[0]
                    ev.y = mouse_y + drag_offset_ev[1]
                    ev.x = max(0, min(ev.x, screen_width - ev.rect.width))
                    ev.y = max(0, min(ev.y, screen_height - ev.rect.height))
                    ev.rect.topleft = (ev.x, ev.y)
                if top_alindi and topun_konumu:
                    # Topu fare imlecinin ucuna taşı
                    topun_konumu = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    kedi.durum = "yuruyor"
                    kedi.hareket.hareket_baslangic_zamani = kedi.istatistikler.besleme_zamanı
                    kedi.animasyonlar.resim_degistirme_zamani = kedi.istatistikler.besleme_zamanı
            ev.handle_event(event, kedi, top_alindi)

        # Ekranı temizle (saydam renkle doldur)
        screen.fill((0, 0, 0, 0))

        # Ev ve kediyi çiz
        ev.ciz(screen)
        kedi.ciz(screen)

        # Eğer top alındıysa, fare imlecinin ucuna çiz
        if top_alindi and topun_konumu:
            ekran_x, ekran_y = topun_konumu
            top_rect = pygame.Rect(ekran_x - 12, ekran_y - 12, 25, 25)  # 12, top resminin yarı genişliği/yüksekliği
            screen.blit(pygame.image.load(os.path.join(ev.PIC_FOLDER, "top.png")).convert_alpha(), top_rect)

        # Kedinin durumunu güncelle
        kedi.guncelle()

        # Ekranı güncelle
        pygame.display.flip()

        # FPS'yi ayarla
        clock.tick(60)