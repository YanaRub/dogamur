import pygame
from pygame import *

pygame.init()
pygame.mixer.init()
music_menu = "pixelated-adventures_92797.mp3"
music_game = "retro"
pygame.mixer.music.load(music_menu)
pygame.mixer.music.play(-1)
playing_music = "menu"

# ==================== CONFIG ====================
WIDTH, HEIGHT = 1200, 700
FPS = 60

back1 = pygame.transform.scale(image.load("back1.jpg"),(WIDTH, HEIGHT))
back2 = pygame.transform.scale(image.load("back2.jpg"),(WIDTH, HEIGHT))
back3 = pygame.transform.scale(image.load("back3.jpg"),(WIDTH, HEIGHT))
platform = pygame.transform.scale(image.load("platform.jpg"),(WIDTH, HEIGHT))
dog = pygame.transform.scale(image.load("dog.jpg"),(80, 120))

menu_bg = pygame.image.load("background.jpg")
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
level1_bg = pygame.image.load("back1.jpg")
level1_bg = pygame.transform.scale(level1_bg, (WIDTH, HEIGHT))

GRAVITY = 0.9
PLAYER_SPEED = 6
JUMP_FORCE = 18

# COLORS
BG = (25, 25, 35)
WHITE = (240, 240, 240)
GRAY = (180, 180, 180)
HOVER = (220, 220, 220)
GREEN = (0, 200, 0)
PLAYER_COLOR = (80, 200, 255)
PLATFORM_COLOR = (200, 200, 200)

# ==================== INIT ====================

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dog Amur")
clock = pygame.time.Clock()
running = True

# ==================== FONTS ====================
title_font = pygame.font.SysFont("comicsansms", 64, bold=True)
button_font = pygame.font.SysFont("comicsansms", 28)

# ==================== GAME STATE ====================
MENU = "menu"
state = MENU
LEVEL1 = "level1"
LEVEL2 = "level2"
LEVEL3 = "level3"
LEVEL4 = "level4"
LEVEL5 = "level5"

score = 0

# ==================== BUTTON ====================
class Bone(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 20)
        self.collected = False
    def draw(self, surface):
        if not self.collected:
            draw.rect(surface,(255, 255, 150), self, border_radius=5)

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = Rect(x, y, w, h)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER if self.rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        label = button_font.render(self.text, True, BG)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (
            event.type == MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# ==================== MENU ====================
start_button = Button("START", WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50)
exit_button = Button("EXIT", WIDTH // 2 - 80, HEIGHT // 2 + 110, 160, 50)

# ==================== PLAYER ====================
class Player(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[K_a] or keys[K_LEFT]: self.vel_x = -PLAYER_SPEED
        if keys[K_d] or keys[K_RIGHT]: self.vel_x = PLAYER_SPEED
        if keys[K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_FORCE
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def move_x(self, platforms):
        self.x += self.vel_x
        for p in platforms:
            if self.colliderect(p):
                if self.vel_x > 0: self.right = p.left
                elif self.vel_x < 0: self.left = p.right

    def move_y(self, platforms):
        self.y += self.vel_y
        self.on_ground = False
        for p in platforms:
            if self.colliderect(p):
                if self.vel_y > 0:
                    self.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.top = p.bottom
                    self.vel_y = 0

    def update(self, platforms):
        self.input()
        self.apply_gravity()
        self.move_x(platforms)
        self.move_y(platforms)

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self)
        

# ==================== LEVEL ====================
platforms1 = [
    Rect(0, HEIGHT - 40, WIDTH, 40),
    Rect(-65, 100, 70, 800),
    Rect(120, 520, 60, 12),
    Rect(260, 460, 50, 12),
    Rect(380, 400, 45, 12),
    Rect(520, 340, 40, 12),
    Rect(650, 280, 35, 12),
    Rect(780, 220, 30, 12),
    Rect(880, 160, 25, 12),
    Rect(1120, 100, 70, 800)
]
platforms2 = [
    Rect(0, HEIGHT - 40, WIDTH, 40),
    Rect(-65, 100, 70, 800),
    Rect(60, 520, 90, 12),
    Rect(180, 480, 70, 12),
    Rect(300, 440, 80, 12),
    Rect(420, 400, 65, 12),
    Rect(540, 360, 75, 12),
    Rect(660, 320, 60, 12),
    Rect(780, 280, 70, 12),
    Rect(900, 240, 55, 12),
    Rect(820, 200, 60, 12),
    Rect(744, 240, 70, 12),
    Rect(460, 280, 65, 12),
    Rect(280, 500, 80, 12),
    Rect(1120, 120, 70, 600)
]
platforms3 = [
    Rect(40, 520, 120, 14),
    Rect(120, 480, 90, 14),
    Rect(190, 440, 70, 14),
    Rect(250, 400, 60, 14),
    Rect(380, 360, 55, 12),
    Rect(440, 320, 45, 12),
    Rect(500, 280, 40, 12),
    Rect(560, 240, 35, 12),
    Rect(620, 200, 30, 12),
    Rect(680, 170, 28, 12),
    Rect(740, 140, 26, 12),
    Rect(1120, 100, 70, 600)
]
platforms4 = [
    Rect(0, HEIGHT - 40, WIDTH, 40),
    Rect(150, 470, 70, 12),
    Rect(620, 430, 60, 12),
    Rect(300, 360, 50, 12),
    Rect(800, 300, 45, 12),
    Rect(420, 240, 40, 12),
    Rect(950, 180, 35, 12),
]
platforms5 = [
    Rect(0, HEIGHT - 40, WIDTH, 40),
    Rect(-65, 100, 70, 800),
    Rect(480, 500, 60, 12),
    Rect(420, 440, 50, 12),
    Rect(520, 380, 45, 12),
    Rect(400, 320, 40, 12),
    Rect(540, 260, 35, 12),
    Rect(380, 200, 30, 12),
    Rect(560, 140, 25, 12),
    Rect(1120, 120, 70, 600)
]
player = Player(100, 100)

bones1 = [Bone(130, 490), Bone(530, 310)]
bones2 = [Bone(70, 490), Bone(790, 250)]
bones3 = [Bone(50, 490), Bone(510, 250)]
bones4 = [Bone(160, 440), Bone(810, 270)]
bones5 = [Bone(490, 470), Bone(550, 230)]

# ==================== MAIN LOOP ====================
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if state == MENU:
            if start_button.clicked(event):
                state = LEVEL1
                score = 0
            if exit_button.clicked(event):
                running = False
        
        if state == LEVEL1 and player.right > WIDTH:
            state = LEVEL2
            player.x, player.y = 0, 100
            player.vel_x, player.vel_y = 0, 0
            
        if state == LEVEL2 and player.right > WIDTH:
            state = LEVEL3
            player.x, player.y = 0, 100
            player.vel_x, player.vel_y = 0, 0

    # ==================== DRAWING ====================
    if state == MENU:
        # 1. Малюємо картинку фону замість screen.fill
        screen.blit(menu_bg, (0, 0))
                
        start_button.draw(screen)
        exit_button.draw(screen)
        if playing_music != "menu":
            mixer.music.load(music_menu)
            mixer.music.play(-1)
            playing.music="menu"

    else:
        # У грі залишаємо звичайний колір фону
        screen.fill(BG)
        
        if playing_music != "game":
            mixer.music.load(music_game)
            mixer.music.play(-1)
            playing.music="game"
        
        current_platforms = platforms1 if state == LEVEL1 else platforms2
        if state == LEVEL1:
            current_platforms = platforms1
        elif state == LEVEL2:
            current_platforms = platforms2
        elif state == LEVEL3:
            current_platforms = platforms3  
        elif state == LEVEL4:
            current_platforms = platforms4
        else:
            current_platforms = platforms5
        player.update(current_platforms)
        for p in current_platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, p)
        player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
