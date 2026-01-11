import pygame

# ==================== CONFIG ====================
WIDTH, HEIGHT = 1200, 700
FPS = 60

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
pygame.display.set_caption("Platformer with Menu")
clock = pygame.time.Clock()
running = True

# ==================== FONTS ====================
title_font = pygame.font.SysFont("comicsansms", 64, bold=True)
button_font = pygame.font.SysFont("comicsansms", 28)

# ==================== GAME STATE ====================
MENU = "menu"
GAME = "game"
state = MENU
LEVEL1 = "level1"
LEVEL2 = "level2"

# ==================== BUTTON ====================
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        color = HOVER if self.rect.collidepoint(mouse) else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        label = button_font.render(self.text, True, BG)
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# ==================== MENU ====================
start_button = Button("START", WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50)
exit_button = Button("EXIT", WIDTH // 2 - 80, HEIGHT // 2 + 110, 160, 50)

# ==================== PLAYER ====================
class Player(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -JUMP_FORCE
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def move_x(self, platforms):
        self.x += self.vel_x
        for p in platforms:
            if self.colliderect(p):
                if self.vel_x > 0:
                    self.right = p.left
                elif self.vel_x < 0:
                    self.left = p.right

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
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(200, 380, 200, 20),
    pygame.Rect(500, 300, 180, 20),
    pygame.Rect(320, 220, 140, 20),
]
platforms2 = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(100, 280, 100, 30),
    pygame.Rect(350, 340, 180, 20),
    pygame.Rect(220, 120, 240, 50),
]

player = Player(100, 100)

# ==================== MAIN LOOP ====================
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU INPUT
        if state == MENU:
            if start_button.clicked(event):
                state = LEVEL1
            if player.right > WIDTH:
                state = LEVEL2
                player.x = 0
                player.y = 100
                player.vel_x = 0
                player.vel_y = 0
            if exit_button.clicked(event):
                running = False

    screen.fill(BG)

    # ==================== MENU ====================
    if state == MENU:
        # green square (logo placeholder)
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 50, 30, 100, 100))

        title = title_font.render("Charpets", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 170)))

        start_button.draw(screen)
        exit_button.draw(screen)

    # ==================== GAME ====================
    elif state == LEVEL1:
        player.update(platforms1)

        for p in platforms1:
            pygame.draw.rect(screen, PLATFORM_COLOR, p)

        player.draw(screen)

    elif state == LEVEL2:
        player.update(platforms2)

        for p in platforms2:
            pygame.draw.rect(screen, PLATFORM_COLOR, p)

        player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()