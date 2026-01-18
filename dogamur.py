from pygame import *
import sys

# ================== ІНІЦІАЛІЗАЦІЯ ==================
init()

# Розмір вікна
WIDTH, HEIGHT = 900, 500
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Dog Amur")

clock = time.Clock()
FPS = 60

# ================== КОЛЬОРИ (ТИМЧАСОВІ) ==================
# ⚠️ КОЛИ БУДУТЬ КАРТИНКИ — ЦЕ МОЖНА ВИДАЛИТИ
WHITE = (255, 255, 255)
BROWN = (160, 110, 60)
BLUE = (120, 180, 255)
GREEN = (80, 170, 80)
BLACK = (0, 0, 0)

# ================== ГРАВЕЦЬ — ПЕС АМУР ==================
# Прямокутник — тимчасова форма персонажа
amur = Rect(100, 350, 40, 50)

# 👉 У МАЙБУТНЬОМУ:
# amur_img = image.load("assets/amur_idle.png").convert_alpha()
# amur_img = transform.scale(amur_img, (40, 50))

amur_speed = 5
jump_power = 14
gravity = 0.8
y_velocity = 0
on_ground = False

# ================== ПЛАТФОРМИ / ОБʼЄКТИ ==================
# Це можуть бути: земля, будинки, ящики, сходи
platforms = [
    Rect(0, 400, WIDTH, 100),      # земля
    Rect(200, 320, 120, 20),       # платформа
    Rect(400, 280, 120, 20),
    Rect(650, 350, 150, 20),
]

# 👉 У МАЙБУТНЬОМУ:
# platform_img = image.load("assets/platform.png").convert_alpha()

# ================== ФОН ==================
# Поки що просто небо
# 👉 Потім: вулиця, двір, підʼїзд, підвал
def draw_background():
    screen.fill(BLUE)

    # 👉 З КАРТИНКОЮ:
    # screen.blit(background_img, (0, 0))


# ================== ФУНКЦІЯ РУХУ ТА ФІЗИКИ ==================
def move_player():
    global y_velocity, on_ground

    keys = key.get_pressed()

    # ---- рух вліво / вправо ----
    if keys[K_a]:
        amur.x -= amur_speed
    if keys[K_d]:
        amur.x += amur_speed

    # ---- стрибок ----
    if keys[K_SPACE] and on_ground:
        y_velocity = -jump_power
        on_ground = False

    # ---- гравітація ----
    y_velocity += gravity
    amur.y += y_velocity

    # ---- перевірка зіткнення з платформами ----
    on_ground = False
    for platform in platforms:
        if amur.colliderect(platform) and y_velocity > 0:
            amur.bottom = platform.top
            y_velocity = 0
            on_ground = True


# ================== ГОЛОВНИЙ ЦИКЛ ГРИ ==================
running = True
while running:
    clock.tick(FPS)

    # ---- події ----
    for e in event.get():
        if e.type == QUIT:
            running = False

    # ---- логіка ----
    move_player()

    # ---- малювання ----
    draw_background()

    # Платформи / обʼєкти світу
    for platform in platforms:
        draw.rect(screen, GREEN, platform)

        # 👉 З КАРТИНКОЮ:
        # screen.blit(platform_img, platform)

    # Пес Амур
    draw.rect(screen, BROWN, amur)

    # 👉 З КАРТИНКОЮ:
    # screen.blit(amur_img, amur)

    display.update()

quit()
sys.exit()
