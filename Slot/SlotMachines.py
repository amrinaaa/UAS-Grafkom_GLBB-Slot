import pygame
import sys
import math
import time

pygame.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lucky Slot - Online Slot Machines")

# Warna
Putih = (255, 255, 255)
Hitam = (0, 0, 0)
Merah = (187, 37, 37)
Kuning = (252, 220, 42)
KuningGelap = (255, 201, 74)
Cokelat = (192, 139, 92)
Hijau = (0, 191, 99)
Background = (50, 38, 83)
Ungu = (128, 98, 214)
Grey = (178, 178, 178)
DarkGrey = (125, 124, 124)
Pink = (255, 64, 125)
Biru = (102,184,201)
BiruLangit = (213, 244, 250)

# Initialize font
font = pygame.font.Font(None, 36)

# DDA konversi koordinat x y
def konv_koor_x(x):
    return screen.get_width() // 2 + x * -1

def konv_koor_y(y):
    return screen.get_height() // 2 + y * -1

def midpoint_draw_ellipse(surface, color, xc, yc, rx, ry):
    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2
    x = 0
    y = ry
    px = 0
    py = two_rx2 * y
    p = round(ry2 - (rx2 * ry) + (0.25 * rx2))
    
    def draw_symmetric_points(surface, color, xc, yc, x, y):
        pygame.draw.circle(surface, color, (xc + x, yc + y), 2)
        pygame.draw.circle(surface, color, (xc - x, yc + y), 2)
        pygame.draw.circle(surface, color, (xc + x, yc - y), 2)
        pygame.draw.circle(surface, color, (xc - x, yc - y), 2)
    
    draw_symmetric_points(surface, color, xc, yc, x, y)
    
    while px < py:
        x += 1
        px += two_ry2
        if p < 0:
            p += ry2 + px
        else:
            y -= 1
            py -= two_rx2
            p += ry2 + px - py
        draw_symmetric_points(surface, color, xc, yc, x, y)
    
    p = round(ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2)
    
    while y > 0:
        y -= 1
        py -= two_rx2
        if p > 0:
            p += rx2 - py
        else:
            x += 1
            px += two_ry2
            p += rx2 - py + px
        draw_symmetric_points(surface, color, xc, yc, x, y)

def midpoint_lingkaran(xc, yc, radius):
    x = radius
    y = 0
    p = 1 - radius

    while x > y:
        y += 1
        
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1
        
        if x < y:
            break

        # Gambar titik-titik yang simetris
        pygame.draw.circle(screen, Putih, (xc + x, yc - y), 1)
        pygame.draw.circle(screen, Putih, (xc - x, yc - y), 1)
        pygame.draw.circle(screen, Putih, (xc + x, yc + y), 1)
        pygame.draw.circle(screen, Putih, (xc - x, yc + y), 1)
        
        if y != x:
            pygame.draw.circle(screen, Putih, (xc + y, yc - x), 1)
            pygame.draw.circle(screen, Putih, (xc - y, yc - x), 1)
            pygame.draw.circle(screen, Putih, (xc + y, yc + x), 1)
            pygame.draw.circle(screen, Putih, (xc - y, yc + x), 1)

def draw_line_dda_objek(x1, y1, x2, y2, color, thickness, anti_aliasing_factor):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return
    steps = max(abs(dx), abs(dy))

    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x1, y1
    for _ in range(int(steps)):
        pygame.draw.circle(screen, color, (round(x), round(y)), thickness)
        # Draw additional points for anti-aliasing
        # for i in range(1, anti_aliasing_factor):
        pygame.draw.circle(screen, color, (round(x + 0.25), round(y + 0.25)), thickness)
        pygame.draw.circle(screen, color, (round(x - 0.25), round(y - 0.25)), thickness)
        pygame.draw.circle(screen, color, (round(x + 0.25), round(y - 0.25)), thickness)
        pygame.draw.circle(screen, color, (round(x - 0.25), round(y + 0.25)), thickness)
        x += x_increment
        y += y_increment

def draw_angka_satu(x_pos1, y_pos1):
    x1, y1 = konv_koor_x(x_pos1), konv_koor_y(y_pos1)
    x2, y2 = konv_koor_x(x_pos1), konv_koor_y(y_pos1 + 80)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    x1, y1 = konv_koor_x(x_pos1), konv_koor_y(y_pos1 + 80)
    x2, y2 = konv_koor_x(x_pos1 + 20), konv_koor_y(y_pos1 + 80 - 10)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

def draw_angka_dua(x_pos2, y_pos2):
    # Gambar bagian atas angka 2
    x1, y1 = konv_koor_x(x_pos2), konv_koor_y(y_pos2)
    x2, y2 = konv_koor_x(x_pos2 + 30), konv_koor_y(y_pos2)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    x1, y1 = konv_koor_x(x_pos2 + 30), konv_koor_y(y_pos2)
    x2, y2 = konv_koor_x(x_pos2 + 30), konv_koor_y(y_pos2 + 40)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)
    x1, y1 = konv_koor_x(x_pos2), konv_koor_y(y_pos2 + 40)
    x2, y2 = konv_koor_x(x_pos2 + 30), konv_koor_y(y_pos2 + 40)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    # Gambar bagian tengah angka 2
    x1, y1 = konv_koor_x(x_pos2), konv_koor_y(y_pos2 + 40)
    x2, y2 = konv_koor_x(x_pos2), konv_koor_y(y_pos2 + 80)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    # Gambar bagian bawah angka 2
    x1, y1 = konv_koor_x(x_pos2), konv_koor_y(y_pos2 + 80)
    x2, y2 = konv_koor_x(x_pos2 + 30), konv_koor_y(y_pos2 + 80)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

def draw_angka_tiga(x_pos3, y_pos3):
    # Gambar bagian atas angka 3
    x1, y1 = konv_koor_x(x_pos3), konv_koor_y(y_pos3)
    x2, y2 = konv_koor_x(x_pos3 + 30), konv_koor_y(y_pos3)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    x1, y1 = konv_koor_x(x_pos3), konv_koor_y(y_pos3)
    x2, y2 = konv_koor_x(x_pos3), konv_koor_y(y_pos3 + 40)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)
    
    x1, y1 = konv_koor_x(x_pos3), konv_koor_y(y_pos3 + 80)
    x2, y2 = konv_koor_x(x_pos3), konv_koor_y(y_pos3 + 40)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    x1, y1 = konv_koor_x(x_pos3), konv_koor_y(y_pos3 + 40)
    x2, y2 = konv_koor_x(x_pos3 + 30), konv_koor_y(y_pos3 + 40)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

    # Gambar bagian tengah angka 3
    x1, y1 = konv_koor_x(x_pos3), konv_koor_y(y_pos3 + 80)
    x2, y2 = konv_koor_x(x_pos3 + 30), konv_koor_y(y_pos3 + 80)
    draw_line_dda_objek(x1, y1, x2, y2, Hitam, 5, 3)

def update_movement(y_pos, speed, count, status, cnt):
    if y_pos == 30:
        count += 1
        if count == cnt:
            status = "berhenti"
    if status == "bergerak":
        y_pos -= speed
    if y_pos == -200 or y_pos <= -200:
        y_pos = 201
    return y_pos, count, status

def update_movement2(y_pos, speed, count, status1, status2 = None):
    if status1 == "berhenti" or status2 == "berhenti":
        status = "berhenti"
    else:
        status = "bergerak"
        y_pos -= speed
    if y_pos == -200 or y_pos <= -200:
            y_pos = 201
    return y_pos, count, status 

def tuas_atas(screen):
    trapesium_points = [(780, 280), (820, 310), (820, 360), (780, 390)]
    pygame.draw.polygon(screen, Biru, trapesium_points)
    pygame.draw.rect(screen, Putih, (820, 315, 58, 37))  # Badan tuas deket trapes
    pygame.draw.rect(screen, Putih, (877, 72, 35, 280))  # Badan tuas

    button_center = (894, 84)
    button_radius = 24
    button_color = Merah
    
    pygame.draw.circle(screen, button_color, button_center, button_radius)
    midpoint_lingkaran(button_center[0], button_center[1], button_radius)  # Memanggil fungsi midpoint_lingkaran yang telah Anda definisikan sebelumnya

    # Ubah warna lingkaran merah jika mouse berada di atasnya
    if is_mouse_over_red_circle:
        pygame.draw.circle(screen, (255, 0, 0), (894, 84), 24)  # Ubah warna ke merah
    else:
        pygame.draw.circle(screen, Merah, (894, 84), 24)

def tuas_bawah(screen):
    trapesium_points = [(780, 280), (820, 310), (820, 360), (780, 390)]
    pygame.draw.polygon(screen, Biru, trapesium_points)
    pygame.draw.rect(screen, Putih, (820, 315, 58, 37))  # Badan tuas deket trapes
    pygame.draw.rect(screen, Putih, (877, 315, 35, 240))  # Badan tuas

    button_center = (894, 560)
    button_radius = 24
    button_color = Merah
    
    pygame.draw.circle(screen, button_color, button_center, button_radius)
    midpoint_lingkaran(button_center[0], button_center[1], button_radius)  

# Memuat gambar
img_tombol = pygame.image.load('Slot/image/spin.png')
img_slot = pygame.image.load('Slot/image/slot.jpg')
img_nama = pygame.image.load('Slot/image/PapanNama.png')
img_lis = pygame.image.load('Slot/image/lis.png')
img_textbox = pygame.image.load('Slot/image/textbox.png')
img_koin = pygame.image.load('Slot/image/koin.png')

# Resize gambar
tombol_width, tombol_height = 210, 70 # Gambar tombol spin 
image_tombol = pygame.transform.scale(img_tombol, (tombol_width, tombol_height))

nama_width, nama_height = 197, 65 # Gambar papan nama 
image_nama = pygame.transform.scale(img_nama, (nama_width, nama_height))

koin_width, koin_height = 270, 54 # Gambar lubang koin
image_koin = pygame.transform.scale(img_koin, (koin_width, koin_height))

textbox_width, textbox_height = 550, 51 # Gambar textbox credit dan bet
image_textbox = pygame.transform.scale(img_textbox, (textbox_width, textbox_height))

lis_width, lis_height = 620, 17 # Gambar garis abu abu  
image_lis = pygame.transform.scale(img_lis, (lis_width, lis_height))

slot_width, slot_height = 480, 250 # Gambar rolling slot
image_slot = pygame.transform.scale(img_slot, (slot_width, slot_height))

tuas_atas_clicked = False
start_time_tuas_bawah = 0
tuas_tampil_atas = True

y_pos1 = y_pos2 = y_pos3 = 30
y_pos11 = y_pos22 = y_pos33 = 162
y_pos111 = y_pos222 = y_pos333 = -107

count1 = count2 = count3 = 0
count11 = count22 = count33 = 0
count111 = count222 = count333 = 0

speed1 = speed2 = speed3 = 1.5
speed11 = speed22 = speed33 = 1.5
speed111 = speed222 = speed333 = 1.5

status1 = status2 = status3 = "bergerak"
status11 = status22 = status33 = "bergerak"
status111 = status222 = status333 = "bergerak"

saldo = "---"

taruhan_per_spin = "---"

saldo_pos = (310, 430)
taruhan_per_spin_pos = (665, 430)

def tampilkan_text():
    saldo_text = font.render(f"{saldo}", True, BiruLangit)
    screen.blit(saldo_text, saldo_pos)
    taruhan_per_spin_text = font.render(f"{taruhan_per_spin}", True, BiruLangit)
    screen.blit(taruhan_per_spin_text , taruhan_per_spin_pos)

spin_pressed_count = 0
start_time = time.time()
loop_count1 = loop_count2 = loop_count3 = loop_count4 = loop_count5 = loop_count6 = loop_count7 = 0
loop_count8 = loop_count9 = loop_count10 = loop_count11 = loop_count12 = loop_count13 = loop_count14 = 0
loop_count15 = loop_count16 = loop_count17 = loop_count18 = loop_count19 = loop_count20 = loop_count21 = 0
spin_reset2 = False
spin_reset3 = False
spin_reset4 = False
spin_reset5 = False
spin_reset6 = False
spin_reset7 = False

# Loop utama
running = True
spin_pressed = False  # Status tombol spin
is_mouse_over_red_circle = False
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            # Cek apakah mouse berada di dalam lingkaran merah
            if math.sqrt((mouse_x - 894)**2 + (mouse_y - 84)**2) <= 24:  # Menggunakan persamaan lingkaran
                is_mouse_over_red_circle = True
            else:
                is_mouse_over_red_circle = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Cek apakah klik terjadi di dalam lingkaran merah
            if math.sqrt((mouse_x - 894)**2 + (mouse_y - 84)**2) <= 24:
                tuas_atas_clicked = True
                berhenti_berputar = False
                tuas_tampil_atas = False  # Tuas atas tidak ditampilkan setelah diklik
                start_time_tuas_bawah = current_time
                spin_pressed_count += 1

    screen.fill((Hitam))

# Di dalam loop utama
    if spin_pressed_count == 1:
        if status1 == "bergerak":
            loop_count1 += 1
            
            if loop_count1 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos1, count1, status1 = update_movement(y_pos1, speed1, count1, status1, 2)
            y_pos22, count22, status22 = update_movement2(y_pos22, speed22, count22, status22)
            y_pos333, count333, status333 = update_movement2(y_pos333, speed333, count333, status333)
        
        elif status2 == "bergerak":
            loop_count2 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count2 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos2, count2, status2 = update_movement(y_pos2, speed2, count2, status2, 2)
            y_pos33, count33, status33 = update_movement2(y_pos33, speed33, count33, status33)
            y_pos111, count111, status111 = update_movement2(y_pos111, speed111, count111, status111)

        elif status3 == "bergerak":
            loop_count3 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count3 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos3, count3, status3 = update_movement(y_pos3, speed3, count3, status3, 2)
            y_pos11, count11, status11 = update_movement2(y_pos11, speed11, count11, status11)
            y_pos222, count222, status222 = update_movement2(y_pos222, speed222, count222, status222)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti" and status2 == "berhenti" and status3 == "berhenti":
            count1 = count2 = count3 = 0
        if status11 == "berhenti" and status22 == "berhenti" and status33 == "berhenti":
            count11 = count22 = count33 = 0
        if status111 == "berhenti" and status222 == "berhenti" and status333 == "berhenti":
            count111 = count222 = count333 = 0
        
    if spin_pressed_count == 2:
        if not spin_reset2:
            status1 = status11 = status111 = status222 = status22 = status2 = status33 = status3 = status333 = "bergerak"
            spin_reset2 = True

        if status1 == "bergerak":
            loop_count4 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count4 <= 175: 
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos22, count22, status22 = update_movement(y_pos22, speed22, count22, status22, 1)
            y_pos333, count333, status333 = update_movement2(y_pos333, speed333, count333, status333, status22)
            y_pos1, count1, status1 = update_movement2(y_pos1, speed1, count1, status1, status22)
        elif status2 == "bergerak":
            loop_count5 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count5 <= 175:  
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos2, count2, status2 = update_movement(y_pos2, speed2, count2, status2, 2)
            y_pos33, count33, status33 = update_movement2(y_pos33, speed33, count33, status33, status2)
            y_pos111, count111, status111 = update_movement2(y_pos111, speed111, count111, status111, status2)

        elif status3 == "bergerak":
            loop_count6 += 1

            if loop_count6 <= 175: 
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos222, count222, status222 = update_movement(y_pos222, speed222, count222, status222, 1)
            y_pos3, count3, status3 = update_movement2(y_pos3, speed3, count3, status3, status222)
            y_pos11, count11, status11 = update_movement2(y_pos11, speed11, count11, status11, status222)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti" and status2 == "berhenti" and status3 == "berhenti":
            count1 = count2 = count3 = 0
        if status11 == "berhenti" and status22 == "berhenti" and status33 == "berhenti":
            count11 = count22 = count33 = 0
        if status111 == "berhenti" and status222 == "berhenti" and status333 == "berhenti":
            count111 = count222 = count333 = 0

    if spin_pressed_count == 3:
        if not spin_reset3:
            status1 = status11 = status111 = status222 = status22 = status2 = status33 = status3 = status333 = "bergerak"
            spin_reset3 = True

        if status1 == "bergerak":
            loop_count7 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count7 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1          
            y_pos333, count333, status333 = update_movement(y_pos333, speed333, count333, status333, 2)
            y_pos22, count22, status22 = update_movement2(y_pos22, speed22, count22, status22, status333)
            y_pos1, count1, status1 = update_movement2(y_pos1, speed1, count1, status1, status333)
        elif status2 == "bergerak":
            loop_count8 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count8 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1            
            y_pos33, count33, status33 = update_movement(y_pos33, speed33, count33, status33, 1)
            y_pos2, count2, status2 = update_movement2(y_pos2, speed2, count2, status2, status33)
            y_pos111, count111, status111 = update_movement2(y_pos111, speed111, count111, status111, status33)
        elif status3 == "bergerak":
            loop_count9 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count9 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1            
            y_pos11, count11, status11 = update_movement(y_pos11, speed11, count11, status11, 1)
            y_pos222, count222, status222 = update_movement2(y_pos222, speed222, count222, status222, status11)
            y_pos3, count3, status3 = update_movement2(y_pos3, speed3, count3, status3, status11)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti":
            count1 = 0
        if status2 == "berhenti":
            count2 = 0
        if status3 == "berhenti":
            count3 = 0
        if status11 == "berhenti":
            count11 = 0
        if status22 == "berhenti":
            count22 = 0
        if status33 == "berhenti":
            count33 = 0
        if status111 == "berhenti":
            count111 = 0
        if status222 == "berhenti":
            count222 = 0
        if status333 == "berhenti":
            count333 = 0

    if spin_pressed_count == 4:
        if not spin_reset4:
            status1 = status11 = status111 = status222 = status22 = status2 = status33 = status3 = status333 = "bergerak"
            spin_reset4 = True

        if status1 == "bergerak":
            loop_count10 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count10 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1          
            y_pos333, count333, status333 = update_movement(y_pos333, speed333, count333, status333, 2)
            y_pos22, count22, status22 = update_movement2(y_pos22, speed22, count22, status22, status333)
            y_pos1, count1, status1 = update_movement2(y_pos1, speed1, count1, status1, status333)
        elif status2 == "bergerak":
            loop_count11 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count11 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos111, count111, status111 = update_movement(y_pos111, speed111, count111, status111, 2)
            y_pos2, count2, status2 = update_movement2(y_pos2, speed2, count2, status2, status111)
            y_pos33, count33, status33 = update_movement2(y_pos33, speed33, count33, status33, status111)
        elif status3 == "bergerak":
            loop_count12 += 1

            if loop_count12 <= 175: 
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos222, count222, status222 = update_movement(y_pos222, speed222, count222, status222, 1)
            y_pos3, count3, status3 = update_movement2(y_pos3, speed3, count3, status3, status222)
            y_pos11, count11, status11 = update_movement2(y_pos11, speed11, count11, status11, status222)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti":
            count1 = 0
        if status2 == "berhenti":
            count2 = 0
        if status3 == "berhenti":
            count3 = 0
        if status11 == "berhenti":
            count11 = 0
        if status22 == "berhenti":
            count22 = 0
        if status33 == "berhenti":
            count33 = 0
        if status111 == "berhenti":
            count111 = 0
        if status222 == "berhenti":
            count222 = 0
        if status333 == "berhenti":
            count333 = 0

    if spin_pressed_count == 5:
        if not spin_reset5:
            status1 = status11 = status111 = status222 = status22 = status2 = status33 = status3 = status333 = "bergerak"
            spin_reset5 = True

        if status1 == "bergerak":
            loop_count13 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count13 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos1, count1, status1 = update_movement(y_pos1, speed1, count1, status1, 2)
            y_pos22, count22, status22 = update_movement2(y_pos22, speed22, count22, status22, status1)
            y_pos333, count333, status333 = update_movement2(y_pos333, speed333, count333, status333, status1)
        elif status2 == "bergerak":
            loop_count14 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count14 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos111, count111, status111 = update_movement(y_pos111, speed111, count111, status111, 2)
            y_pos2, count2, status2 = update_movement2(y_pos2, speed2, count2, status2, status111)
            y_pos33, count33, status33 = update_movement2(y_pos33, speed33, count33, status33, status111)
        elif status3 == "bergerak":
            loop_count15 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count15 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos11, count11, status11 = update_movement(y_pos11, speed11, count11, status11, 2)
            y_pos222, count222, status222 = update_movement2(y_pos222, speed222, count222, status222, status11)
            y_pos3, count3, status3 = update_movement2(y_pos3, speed3, count3, status3, status11)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti":
            count1 = 0
        if status2 == "berhenti":
            count2 = 0
        if status3 == "berhenti":
            count3 = 0
        if status11 == "berhenti":
            count11 = 0
        if status22 == "berhenti":
            count22 = 0
        if status33 == "berhenti":
            count33 = 0
        if status111 == "berhenti":
            count111 = 0
        if status222 == "berhenti":
            count222 = 0
        if status333 == "berhenti":
            count333 = 0

    if spin_pressed_count == 6:
        if not spin_reset6:
            status1 = status11 = status111 = status222 = status22 = status2 = status33 = status3 = status333 = "bergerak"
            spin_reset6 = True

        if status1 == "bergerak":
            loop_count16 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count16 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos1, count1, status1 = update_movement(y_pos1, speed1, count1, status1, 2)
            y_pos22, count22, status22 = update_movement2(y_pos22, speed22, count22, status22, status1)
            y_pos333, count333, status333 = update_movement2(y_pos333, speed333, count333, status333, status1)
        elif status2 == "bergerak":
            loop_count17 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count17 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos33, count33, status33 = update_movement(y_pos33, speed33, count33, status33, 2)
            y_pos111, count111, status111 = update_movement2(y_pos111, speed111, count111, status33)
            y_pos2, count2, status2 = update_movement2(y_pos2, speed2, count2, status2, status33)
        elif status3 == "bergerak":
            loop_count18 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count18 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1    
            y_pos11, count11, status11 = update_movement(y_pos11, speed11, count11, status11, 2)
            y_pos222, count222, status222 = update_movement2(y_pos222, speed222, count222, status222, status11)
            y_pos3, count3, status3 = update_movement2(y_pos3, speed3, count3, status3, status11)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti":
            count1 = 0
        if status2 == "berhenti":
            count2 = 0
        if status3 == "berhenti":
            count3 = 0
        if status11 == "berhenti":
            count11 = 0
        if status22 == "berhenti":
            count22 = 0
        if status33 == "berhenti":
            count33 = 0
        if status111 == "berhenti":
            count111 = 0
        if status222 == "berhenti":
            count222 = 0
        if status333 == "berhenti":
            count333 = 0
    
    if spin_pressed_count == 7:
        if not spin_reset7:
            status1 = status11 = status111 = status222 = status22 = status2 = status33 = status3 = status333 = "bergerak"
            spin_reset7 = True

        if status1 == "bergerak":
            loop_count19 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count19 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1          
            y_pos333, count333, status333 = update_movement(y_pos333, speed333, count333, status333, 2)
            y_pos22, count22, status22 = update_movement2(y_pos22, speed22, count22, status22, status333)
            y_pos1, count1, status1 = update_movement2(y_pos1, speed1, count1, status1, status333)
        elif status2 == "bergerak":
            loop_count20 += 1
            
            # Setel kecepatan menjadi 3 selama 3 detik pertama
            if loop_count20 <= 175:  # 180 iterasi x 0.0166667 detik per iterasi = 3 detik
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                # Setelah 3 detik, kembalikan kecepatan ke 1
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1            
            y_pos33, count33, status33 = update_movement(y_pos33, speed33, count33, status33, 1)
            y_pos2, count2, status2 = update_movement2(y_pos2, speed2, count2, status2, status33)
            y_pos111, count111, status111 = update_movement2(y_pos111, speed111, count111, status111, status33)
        elif status3 == "bergerak":
            loop_count21 += 1

            if loop_count21 <= 175: 
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 11
            else:
                speed1 = speed11 = speed111 = speed2 = speed22 = speed222 = speed3 = speed33 = speed333 = 1

            y_pos222, count222, status222 = update_movement(y_pos222, speed222, count222, status222, 1)
            y_pos3, count3, status3 = update_movement2(y_pos3, speed3, count3, status3, status222)
            y_pos11, count11, status11 = update_movement2(y_pos11, speed11, count11, status11, status222)

        # Periksa apakah semua baris telah berhenti
        if status1 == "berhenti":
            count1 = 0
        if status2 == "berhenti":
            count2 = 0
        if status3 == "berhenti":
            count3 = 0
        if status11 == "berhenti":
            count11 = 0
        if status22 == "berhenti":
            count22 = 0
        if status33 == "berhenti":
            count33 = 0
        if status111 == "berhenti":
            count111 = 0
        if status222 == "berhenti":
            count222 = 0
        if status333 == "berhenti":
            count333 = 0

    # Gambar gambar ke layar
    screen.blit(image_slot, (257, 100))

    draw_angka_satu(150, y_pos1)
    draw_angka_dua(150, y_pos22)
    draw_angka_tiga(150, y_pos333)

    draw_angka_dua(0, y_pos2)
    draw_angka_tiga(0, y_pos33)
    draw_angka_satu(0, y_pos111)

    draw_angka_tiga(-170, y_pos3)
    draw_angka_satu(-170, y_pos11)
    draw_angka_dua(-170, y_pos222)

    # Render count value as text
    text1 = font.render("KALAH", True, (Putih))
    text2 = font.render("MENANG", True, (Putih))
    text3 = font.render("KALAH", True, (Putih))
    text4 = font.render("KALAH", True, (Putih))
    text5 = font.render("MENANG", True, (Putih))
    text6 = font.render("KALAH", True, (Putih))
    text7 = font.render("KALAH", True, (Putih))

    # Draw text on screen
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 30))
    screen.blit(text3, (10, 50))
    screen.blit(text4, (10, 70))
    screen.blit(text5, (10, 90))
    screen.blit(text6, (10, 110))
    screen.blit(text7, (10, 130))

    # Garis dalam
    x1, y1 = 260, 100
    x2, y2 = 740, 100
    draw_line_dda_objek(x1, y1, x2, y2, Putih, 3, 3) # atas
    draw_line_dda_objek(x1, 350, x2, 350, Putih, 3, 3) # bawah
    draw_line_dda_objek(x1, y1, 260, 350, Putih, 3, 3) # kiri
    draw_line_dda_objek(740, y1, x2, 350, Putih, 3, 3) # kanan

    # Garis luar
    posisi = (220, 30)
    ukuran = (560, 20)
    pygame.draw.rect(screen, Grey, (posisi, ukuran)) # atas
    posisi = (220, 50)
    ukuran = (20, 350)
    pygame.draw.rect(screen, Grey, (posisi, ukuran)) # kiri
    posisi = (760, 50)
    ukuran = (20, 350)
    pygame.draw.rect(screen, Grey, (posisi, ukuran)) # kanan

    # Persegi atas dan bawah
    posisi = (240, 50)
    ukuran = (520, 50)
    pygame.draw.rect(screen, Ungu, (posisi, ukuran)) # atas
    posisi = (240, 350)
    ukuran = (520, 50)
    pygame.draw.rect(screen, Ungu, (posisi, ukuran)) # bawah

    # Persegi kanan dan kiri
    posisi = (240, 50)
    ukuran = (20, 350)
    pygame.draw.rect(screen, Ungu, (posisi, ukuran)) # kiri
    posisi = (740, 50)
    ukuran = (20, 350)
    pygame.draw.rect(screen, Ungu, (posisi, ukuran)) # kanan

    # Persegi badan
    posisi = (220, 400)
    ukuran = (560, 100)
    pygame.draw.rect(screen, Grey, (posisi, ukuran)) # kotak atas
    posisi = (200, 499)
    ukuran = (600, 100)
    pygame.draw.rect(screen, Grey, (posisi, ukuran)) # kotak bawah
    posisi = (220, 519)
    ukuran = (560, 80)
    pygame.draw.rect(screen, DarkGrey, (posisi, ukuran)) # kotak bawah dark grey

    points = [(780, 400), (800, 499), (760, 499)]
    pygame.draw.polygon(screen, Grey, points) # segitiga kanan
    points = [(220, 400), (240, 499), (200, 499)]
    pygame.draw.polygon(screen, Grey, points)  # segitiga kiri

    points = [(240, 200), (275, 225), (240, 255)]
    pygame.draw.polygon(screen, Background, points) # backgorund pointer kiri
    points = [(245, 210), (267, 225), (245, 245)]
    pygame.draw.polygon(screen, Pink, points) # pointer segitiga kiri

    points = [(760, 200), (725, 225), (760, 255)]
    pygame.draw.polygon(screen, Background, points) # backgorund pointer kanan
    points = [(755, 210), (733, 225), (755, 245)]
    pygame.draw.polygon(screen, Pink, points) # pointer segitiga kanan

    screen.blit(image_tombol, (395, 420)) # gambar tombol spin

    midpoint_lingkaran(278, 376, 16) 
    pygame.draw.circle(screen, Merah, (278, 376), 14) # lampu merah kiri
    midpoint_lingkaran(317, 376, 16)
    pygame.draw.circle(screen, Kuning, (317, 376), 14) # lampu kuning kiri
    midpoint_lingkaran(356, 376, 16)
    pygame.draw.circle(screen, Hijau, (356, 376), 14) # lampu hijau kiri

    midpoint_lingkaran(720, 376, 16)
    pygame.draw.circle(screen, Kuning, (720, 376), 14) # lampu kuning kanan 
    midpoint_lingkaran(681, 376, 16)
    pygame.draw.circle(screen, Hijau, (681, 376), 14) # lampu hijau kanan
    midpoint_lingkaran(642, 376, 16)
    pygame.draw.circle(screen, Merah, (642, 376), 14) # lampu merah kanan

    midpoint_draw_ellipse(screen, BiruLangit, 500, 46, 130, 40) # border elipse
    pygame.draw.ellipse(screen, Biru, (379, 10, 243, 72), 0) # gambar elipse papan nama
    screen.blit(image_nama, (403, 12)) # gambar nama
    screen.blit(image_lis, (190, 489)) # gambar garis abu-abu
    screen.blit(image_koin, (360, 530)) # gambar lubang koin
    screen.blit(image_textbox, (223, 416)) # gambar textbox credits dan bet

    tampilkan_text()

    if tuas_tampil_atas:
        tuas_atas(screen)
    else:
        if current_time - start_time_tuas_bawah >= 1000:
            tuas_tampil_atas=True
        else:
            tuas_bawah(screen)

    pygame.display.flip()

# Keluar dari Pygame
pygame.quit()
sys.exit()
