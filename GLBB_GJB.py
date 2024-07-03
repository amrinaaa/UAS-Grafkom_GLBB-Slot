import pygame
import sys
import math
import time
import pygame.gfxdraw
import random

# Inisialisasi Pygame
pygame.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 20, 147)
dimgrey = (105, 105, 105)
darkgrey = (49, 54, 63)
lightgrey = (127, 132, 135)
abuterang = (216, 216, 216)
hitamabu =  (24, 24, 24)
PURPLE = (128, 0, 128)

# Lebar dan tinggi layar
WIDTH, HEIGHT = 1370, 710

# Inisialisasi layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gerak Lurus Berubah Beraturan")

# Variabel untuk slider horizontal (kiri-kanan)
slider_x = WIDTH // 2
slider_width = 150
slider_height = 10
slider_dragging_x = False

# Variabel untuk slider vertikal (atas-bawah)
slider_y = HEIGHT // 2
slider_height_vertical = 150
slider_dragging_y = False

# Variabel untuk lingkaran
radius = 75
circle_x = WIDTH // 2
circle_y = HEIGHT // 2

# Variabel untuk kecepatan bola
velocity = 20

# Variabel untuk sudut rotasi garis silang
angle = 0

# Variabel untuk gravitasi
gravitasi = False

kecepatan_btn = False

# Variabel untuk menyimpan ketinggian bola saat tombol gravitasi aktif
falling_height = 0

# Variabel untuk menentukan apakah gravitasi pertama kali diaktifkan
first_gravity = False

# Variabel untuk menentukan apakah bola sudah jatuh setelah pergerakan slider y
ball_fallen = False
ball_dorong = False

gravity = 0.5
restitusi = 0.5

# Variabel untuk lingkaran
bola = {
    "posX": slider_x,
    "posY": slider_y,
    "velocityY": velocity,
    "velocityX": velocity,
    "restitusi": restitusi,
    "radius": radius,
    "isMovingBackwards": False
}

def konv_koor_y(y):
    return screen.get_height() - y

# Fungsi untuk menggambar slider horizontal
def draw_slider_x():
    pygame.draw.rect(screen, dimgrey, (WIDTH-1220, HEIGHT - 50, WIDTH, HEIGHT-50))
    pygame.draw.rect(screen, WHITE, (WIDTH-1215, HEIGHT - 30, WIDTH-202, slider_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (slider_x - slider_width // 2, HEIGHT - 30, slider_width, slider_height), border_radius=10)
    font = pygame.font.SysFont(None, 25)
    text = font.render("X", True, WHITE)
    screen.blit(text, (WIDTH - 45, HEIGHT - 33))

# Fungsi untuk menggambar slider vertikal
def draw_slider_y():
    pygame.draw.rect(screen, dimgrey, (WIDTH- 50, 0, 50, HEIGHT-50))
    pygame.draw.rect(screen, WHITE, (WIDTH - 30, 5, slider_height, HEIGHT - 52), border_radius=10)
    pygame.draw.rect(screen, BLACK, (WIDTH - 30, slider_y - slider_height_vertical // 2, slider_height, slider_height_vertical), border_radius=10)
    font = pygame.font.SysFont(None, 25)
    text = font.render("Y", True, WHITE)
    screen.blit(text, (WIDTH - 32, HEIGHT - 33))

def kotak_menu():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH-1220, HEIGHT))
    pygame.draw.rect(screen, darkgrey, (0, 0, WIDTH-1220, HEIGHT), 3)

# Fungsi untuk menggambar tombol gravitasi
def draw_gravity_button():
    if gravitasi:
        pygame.draw.rect(screen, WHITE, (13, 155, 104, 35), border_radius=100)
        pygame.draw.rect(screen, darkgrey, (15, 157, 100, 30), border_radius=100)
    else:
        pygame.draw.rect(screen, WHITE, (13, 155, 104, 35), border_radius=100)
        pygame.draw.rect(screen, BLACK, (15, 157, 100, 30), border_radius=100)
    font = pygame.font.SysFont(None, 18)
    text = font.render("GRAVITASI", True, BLUE)
    screen.blit(text, (31, 166, 100, 30))

# Fungsi untuk menghitung perpindahan bola
def calculate_displacement(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return delta_x, delta_y

# Fungsi untuk menentukan ukuran bola
def calculate_ball_size(radius_x, radius_y, magnification):
    new_radius_x = radius_x * magnification
    new_radius_y = radius_y * magnification
    return new_radius_x, new_radius_y

def update_bola():
    global bola, slider_x, slider_y, ball_fallen, new_restitution

    if not ball_fallen:
        isMovingBackwards = bola["isMovingBackwards"]
        newVelocityY = bola["velocityY"] + 0.1
        newVelocityX = bola["velocityX"]
        new_restitution = bola["restitusi"]

        if first_gravity:
            newVelocityY -= gravity*9

        if bola["posX"] > WIDTH - 70:
            isMovingBackwards = True
        elif bola["posX"] < WIDTH - 1215 :
            isMovingBackwards = False

        if isMovingBackwards:
            newVelocityX = -1.8
        else:
            newVelocityX = 1.8

        newY = math.floor(bola["posY"] - newVelocityY)
        newX = math.floor(bola["posX"] + newVelocityX)

        # Jika bola mencapai batas bawah layar
        if newY >= HEIGHT - 47 - slider_height_vertical // 2:
            newY = HEIGHT - 47 - slider_height_vertical // 2
            
            bola["restitusi"] -= 0.05
            newVelocityY = -bola["velocityY"] * bola["restitusi"]
            newVelocityX = -bola["velocityX"] * bola["restitusi"]

            if bola["restitusi"] <= 0:
                ball_fallen = True  # Stop pergerakan bola jika restitusi mencapai 0
                bola["restitusi"] = 0
                # Set kecepatan bola menjadi 0
                bola["velocityX"] = 0
                bola["velocityY"] = 0
                newY = bola["posY"]
                newX = bola["posX"]
                if ball_fallen == False and newVelocityX == 0 and newVelocityY==0:
                    bola["velocityX"] = 0
                    newX = bola["posX"]
                
        # Jika bola mencapai batas atas layar
        elif newY <= bola["radius"]:
            newY = bola["radius"]
            bola["restitusi"] -= 0.05
            newVelocityY = -bola["velocityY"] * bola["restitusi"]
            if bola["restitusi"] <= 0:
                ball_fallen = False  # Stop pergerakan bola jika restitusi mencapai 0
                bola["restitusi"] = 0
                # Set kecepatan bola menjadi 0
                bola["velocityX"] = 0
                bola["velocityY"] = 0
                newY = bola["posY"]
                newX = bola["posX"]

        # Perbarui posisi bola
        bola["posY"] = newY
        bola["posX"] = newX
        bola["velocityX"] = newVelocityX            
        bola["velocityY"] = newVelocityY

        inverted_height = HEIGHT - bola["posY"]  # Tinggi bola terbalik
        bola["radius"] = max(30, int((-0.0012 * inverted_height + 1.15) * 100))  # Update radius sesuai tinggi

        bola["isMovingBackwards"] = isMovingBackwards
        # Set posisi slider x dan slider y ke posisi bola
        slider_x = bola["posX"]
        slider_y = bola["posY"]

# Variabel untuk slider restitusi
restitution_slider_x = 15
restitution_slider_y = 120
restitution_slider_width = 100
restitution_slider_height = 10
restitution_min = 0
restitution_max = 1.0
restitution_dragging = False

# Fungsi untuk menggambar slider restitusi
def draw_restitution_slider():
    # Garis horizontal slider
    pygame.draw.rect(screen, lightgrey, (restitution_slider_x, restitution_slider_y, restitution_slider_width, restitution_slider_height), border_radius=10)

    # Pegangan slider
    pegangan_pos = int((bola["restitusi"]- restitution_min) / (restitution_max - restitution_min) * (restitution_slider_width - 10))
    pygame.draw.circle(screen, WHITE, (restitution_slider_x + pegangan_pos + 5, restitution_slider_y + restitution_slider_height // 2), 10)

    # Teks nilai restitusi (warna biru)
    font = pygame.font.SysFont(None, 24)
    text_blue = font.render("Restitusi: ", True, BLUE)
    screen.blit(text_blue, (restitution_slider_x + restitution_slider_width - restitution_slider_width, restitution_slider_y - 25))

    # Teks nilai restitusi (warna putih)
    font = pygame.font.SysFont(None, 20)
    text_value = font.render("{:.1f}".format(bola["restitusi"]), True, WHITE)
    screen.blit(text_value, (restitution_slider_x + restitution_slider_width - restitution_slider_width + text_blue.get_width(), restitution_slider_y - 25))

# Fungsi untuk mengatur nilai restitusi berdasarkan posisi slider
def set_restitution_from_slider(pos):
    global restitution
    normalized_pos = max(0, min(1, pos / restitution_slider_width))
    bola["restitusi"] = restitution_min + normalized_pos * (restitution_max - restitution_min)

# Fungsi untuk menghitung jarak antara dua titik
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def plot(surface, color, x, y, alpha):
    """Plot the pixel with the given alpha value for anti-aliasing."""
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        base_color = surface.get_at((x, y))
        blended_color = (
            int(color[0] * alpha + base_color[0] * (1 - alpha)),
            int(color[1] * alpha + base_color[1] * (1 - alpha)),
            int(color[2] * alpha + base_color[2] * (1 - alpha))
        )
        surface.set_at((x, y), blended_color)

def draw_circle_filled(surface, color, center, radius):
    """Draw a filled circle using the midpoint algorithm."""
    cx, cy = center
    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if x*x + y*y <= radius*radius:
                surface.set_at((cx + x, cy + y), color)

def draw_circle_anti_aliasing(surface, color, center, radius):
    """Draw the anti-aliased edges of the circle using Xiaolin Wu's algorithm."""
    cx, cy = center
    r = radius

    def draw_circle_points(x, y, alpha):
        plot(surface, color, cx + x, cy + y, alpha)
        plot(surface, color, cx - x, cy + y, alpha)
        plot(surface, color, cx + x, cy - y, alpha)
        plot(surface, color, cx - x, cy - y, alpha)
        plot(surface, color, cx + y, cy + x, alpha)
        plot(surface, color, cx - y, cy + x, alpha)
        plot(surface, color, cx + y, cy - x, alpha)
        plot(surface, color, cx - y, cy - x, alpha)

    x = r
    y = 0
    p = 1 - r
    while x >= y:
        draw_circle_points(x, y, 1 - (p / (2 * r)))
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1

# def draw_antialiased_line(screen, color, start, end):
def plot(surface, color, x, y, alpha):
    """Plot the pixel with the given alpha value for anti-aliasing."""
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        base_color = surface.get_at((x, y))[:3]  # Ensure base_color has size 3 (R, G, B)
        blended_color = (
            min(max(int(color[0] * alpha + base_color[0] * (1 - alpha)), 0), 255),
            min(max(int(color[1] * alpha + base_color[1] * (1 - alpha)), 0), 255),
            min(max(int(color[2] * alpha + base_color[2] * (1 - alpha)), 0), 255)
        )
        surface.set_at((x, y), blended_color)

def draw_antialiased_line(screen, color, start, end):
    def plot(x, y, c):
        """Plot the pixel with brightness c (where 0 ≤ c ≤ 1)."""
        if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
            base_color = screen.get_at((x, y))
            blended_color = (
                int(color[0] * c + base_color[0] * (1 - c)),
                int(color[1] * c + base_color[1] * (1 - c)),
                int(color[2] * c + base_color[2] * (1 - c))
            )
            screen.set_at((x, y), blended_color)

    def ipart(x):
        return int(x)

    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1 - fpart(x)

    x1, y1 = start
    x2, y2 = end
    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    gradient = dy / dx if dx != 0 else 1

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend
    ypxl1 = ipart(yend)

    if steep:
        plot(ypxl1, xpxl1, rfpart(yend) * xgap)
        plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
    else:
        plot(xpxl1, ypxl1, rfpart(yend) * xgap)
        plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

    intery = yend + gradient

    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend
    ypxl2 = ipart(yend)

    if steep:
        plot(ypxl2, xpxl2, rfpart(yend) * xgap)
        plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
    else:
        plot(xpxl2, ypxl2, rfpart(yend) * xgap)
        plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    if steep:
        for x in range(xpxl1 + 1, xpxl2):
            plot(ipart(intery), x, rfpart(intery))
            plot(ipart(intery) + 1, x, fpart(intery))
            intery += gradient
    else:
        for x in range(xpxl1 + 1, xpxl2):
            plot(x, ipart(intery), rfpart(intery))
            plot(x, ipart(intery) + 1, fpart(intery))
            intery += gradient

# Contoh penggunaan draw_antialiased_line dalam fungsi draw_antialiased_cross_lines dan draw_antialiased_diameter
def draw_antialiased_cross_lines(screen, color, center, radius, angle):
    def rotate_point(point, angle, center):
        angle = math.radians(angle)
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        px, py = point
        cx, cy = center
        nx = cos_theta * (px - cx) - sin_theta * (py - cy) + cx
        ny = sin_theta * (px - cx) + cos_theta * (py - cy) + cy
        return (int(nx), int(ny))

    # Hitung posisi titik ujung garis berdasarkan rotasi
    rotated_lines1 = rotate_point((center[0] + radius, center[1]), angle, center)
    rotated_lines2 = rotate_point((center[0], center[1] + radius), angle, center)

    # Gambar garis silang pada bola dengan efek anti-aliasing
    draw_antialiased_line(screen, color, center, rotated_lines1)
    draw_antialiased_line(screen, color, center, rotated_lines2)

def rotasi_garis_silang(screen, color, circle_center, radius, angle):
    cx, cy = circle_center

    # Hitung titik ujung garis diagonal berdasarkan sudut rotasi
    rotated_x1 = int(cx + radius * math.cos(math.radians(angle)))
    rotated_y1 = int(cy - radius * math.sin(math.radians(angle)))
    rotated_x2 = int(cx - radius * math.cos(math.radians(angle)))
    rotated_y2 = int(cy + radius * math.sin(math.radians(angle)))

    # Gambar garis diagonal dengan sudut rotasi yang tepat
    draw_antialiased_line(screen, color, (rotated_x1, rotated_y1), (rotated_x2, rotated_y2))

def draw_star(surface, x, y, size, color):
    outer_radius = size
    inner_radius = size // 2
    num_points = 10
    angle = -math.pi / 2
    angle_increment = math.pi * 2 / num_points
    points = []
    for _ in range(num_points * 2):
        radius = outer_radius if len(points) % 2 == 0 else inner_radius
        points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
        angle += angle_increment
    pygame.draw.polygon(surface, color, points)

# Inisialisasi daftar bintang
bintang_list = []
for _ in range(20):
    bintang = {
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': 1,
        'angle': random.uniform(0, 360),
        'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    }
    bintang_list.append(bintang)

background_image = pygame.image.load('GLBB/image/awan.jpg')
kartun = pygame.image.load('GLBB/image/rumput.jpg')

background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
kartun = pygame.transform.scale(kartun, (WIDTH, HEIGHT - 40))

fade_in = True
running = True
fullscreen = False
alpha = 0
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.Rect(13, 155, 104, 35).collidepoint(event.pos):
                    gravitasi = not gravitasi
                    first_gravity = not first_gravity
                elif pygame.Rect(slider_x - slider_width // 2, HEIGHT - 30, slider_width, slider_height).collidepoint(event.pos):
                    slider_dragging_x = True
                elif pygame.Rect(WIDTH - 30, slider_y - slider_height_vertical // 2, slider_height, slider_height_vertical).collidepoint(event.pos):
                    slider_dragging_y = True
                elif pygame.Rect(restitution_slider_x, restitution_slider_y, restitution_slider_width, restitution_slider_height).collidepoint(event.pos):
                    restitution_dragging = True
                    ball_fallen = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_dragging_x = False
                slider_dragging_y = False
                ball_fallen = True
                if slider_dragging_x == True and slider_dragging_y == True:
                    ball_fallen = True
                if restitution_dragging:
                    restitution_slider_mouse_x, _ = event.pos
                    new_restitution_pos = restitution_slider_mouse_x - restitution_slider_x
                    set_restitution_from_slider(new_restitution_pos)
                    restitution_dragging = False
                    if bola["posY"] == HEIGHT -47 - slider_height_vertical//2:
                        ball_fallen = True
                    else:
                        ball_fallen = False
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                if slider_dragging_x:
                    slider_x = event.pos[0]
                    if slider_x < slider_width // 2:
                        slider_x = slider_width // 2
                    elif slider_x > WIDTH - slider_width // 2:
                        slider_x = WIDTH - slider_width // 2
                    bola["posX"] = slider_x
                    angle = -(slider_x - WIDTH // 2) * 1.8
                elif slider_dragging_y:
                    slider_y = event.pos[1]
                    if slider_y < slider_height_vertical // 2:
                        slider_y = slider_height_vertical // 2
                    elif slider_y > HEIGHT-47 - slider_height_vertical // 2:
                        slider_y = HEIGHT-47 - slider_height_vertical // 2
                    bola["posY"] = slider_y
                bola["posX"], bola["posY"] = slider_x, slider_y
            if event.buttons[0] == 1:
                if restitution_dragging:
                    restitution_slider_mouse_x, _ = event.pos
                    new_restitution_pos = restitution_slider_mouse_x - restitution_slider_x
                    set_restitution_from_slider(new_restitution_pos)

    update_bola()

    if not gravitasi:
        if fade_in:
            temp_surface = background_image.copy()
            temp_surface.set_alpha(alpha)
            screen.fill(WHITE)  # Isi layar dengan warna putih
            screen.blit(temp_surface, (0, 0))
            alpha += 5  # Tingkatkan alpha untuk efek fade-in
            if alpha >= 255:
                alpha = 255
            fade_in = False
        else:
            screen.blit(background_image, (0, 0))
        for bintang in bintang_list:
            x = bintang['x']
            y = bintang['y']
            color = bintang['color']
            draw_star(screen, x, y, 20, color)
            # Update posisi bintang berdasarkan kecepatan dan arahnya
            radian_angle = math.radians(bintang['angle'])
            x_change = bintang['speed'] * math.cos(radian_angle)
            y_change = bintang['speed'] * math.sin(radian_angle)
            bintang['x'] += x_change
            bintang['y'] += y_change
            # Memastikan bintang tetap berada di dalam area layar
            if bintang['x'] < 0 or bintang['x'] > WIDTH or bintang['y'] < 0 or bintang['y'] > HEIGHT:
                bintang['x'] = random.randint(0, WIDTH)
                bintang['y'] = random.randint(0, HEIGHT)
                bintang['angle'] = random.uniform(0, 360)
    elif gravitasi:
        screen.blit(kartun, (0, 0))

    normalized_slider_pos_x = (slider_x - slider_width // 2) / (WIDTH - slider_width) * 100
    normalized_slider_pos_y = (slider_y - slider_height_vertical // 2) / (HEIGHT - slider_height_vertical) * 100
    
    magnification = 0.5

    circle_x = int(normalized_slider_pos_x / 100 * (WIDTH - 2 * radius)) + radius
    circle_y = int(normalized_slider_pos_y / 100 * (HEIGHT - 2 * radius)) + radius

    circle_x = bola["posX"]
    circle_y = bola["posY"]
    # angle = 0
    
    adjusted_radius = radius - (slider_y - slider_height_vertical // 2) / (HEIGHT - slider_height_vertical) * -radius
    new_radius_x, new_radius_y = calculate_ball_size(adjusted_radius, adjusted_radius, magnification)

    draw_circle_filled(screen, abuterang, (circle_x, circle_y), int(new_radius_x))
    draw_circle_anti_aliasing(screen, abuterang, (circle_x, circle_y), int(new_radius_x))

    rotasi_garis_silang (screen, BLUE, (circle_x, circle_y), int(new_radius_x), angle)
    rotasi_garis_silang (screen, PINK, (circle_x, circle_y), int(new_radius_x), angle + 90)

    delta_x, delta_y = calculate_displacement(circle_x, circle_y, circle_x + 1, circle_y + 1)

    # Update sudut rotasi berdasarkan pergerakan slider horizontal
    angle = -(slider_x - WIDTH // 2) * 1.8

    # Cek agar slider vertikal tidak melewati batas slider vertical
    if slider_y - slider_height_vertical // 2 + 5 < 0:
        slider_y = slider_height_vertical // 2 + 5
    elif slider_y + slider_height_vertical // 2 > HEIGHT - 46.5:
        slider_y = HEIGHT - 46.5 - slider_height_vertical // 2

    # Batasi pergerakan slider horizontal dan rect menu
    if slider_x - slider_width // 2 < WIDTH - 1215:
        slider_x = WIDTH - 1215 + slider_width // 2
    elif slider_x + slider_width // 2 > WIDTH - 47:
        slider_x = WIDTH - 47 - slider_width // 2

    draw_slider_x()
    draw_slider_y()
    kotak_menu()
    draw_gravity_button()
    draw_restitution_slider()
    
    konv_circle_y = konv_koor_y(circle_y)
    font = pygame.font.SysFont(None, 24)
    text = font.render("Posisi Bola:", True, BLUE)
    screen.blit(text, (15, 30))
    font = pygame.font.SysFont(None, 20)
    text = font.render(f"(X, Y): ({int(circle_x)}, {int(konv_circle_y)})", True, WHITE)
    screen.blit(text, (15, konv_koor_y(HEIGHT-60)))

    pygame.display.flip()
    
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
