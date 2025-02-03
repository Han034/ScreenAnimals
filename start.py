import pygame
import win32api
import win32con
import win32gui
import os
from cat.cat import Kedi
from cat_house import KediEvi
from game_cyc import oyun_dongusu

# Pygame'i başlat
pygame.init()

# TAM EKRAN boyutlarını al
screen_width = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)

# Pencereyi TAM EKRAN ve ÇERÇEVESİZ yap
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

# Arkaplan rengini saydam yap
background_color = (0, 0, 0, 0)

# Ev ve kedi objelerini oluştur
ev = KediEvi(screen_width * 3 / 4, screen_height / 2, screen_width, screen_height)
kedi = Kedi(screen_width / 4, screen_height / 2, screen_width, screen_height, ev)

# Fontu başlat
font = pygame.font.Font(None, 30)

# Görselleri yükle
PIC_FOLDER = os.path.join(os.path.dirname(__file__), "pic")
# Kedi görselleri yüklenirken kullanılan kodlar cat.py içerisinde
# KediEvi görselleri yüklenirken kullanılan kodlar cat_house.py içerisinde
# Top görselleri yüklenirken kullanılan kodlar top.py içerisinde

# Pencereyi saydam yap (Sadece Windows için)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*background_color[:3]), 0, win32con.LWA_COLORKEY)

# Pencereyi HER ZAMAN EN ÜSTTE yap
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# Oyun döngüsünü başlat
oyun_dongusu(screen, screen_width, screen_height, kedi, ev)

pygame.quit()