button_font = pygame.font.SysFont("comicsansms", 28)
score_font = pygame.font.SysFont("comicsansms", 36, bold=True)

MENU = "menu"
LEVEL1 = "level1"
LEVEL2 = "level2"
LEVEL3 = "level3"
LEVEL4 = "level4"
LEVEL5 = "level5"
state = MENU
score = 0


class Bone(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 50)
        self.collected = False
        self.image = pygame.image.load("bone2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.topleft)

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = Rect(x, y, w, h)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = HOVER if self.rect.collidepoint(mouse_pos) else GRAY
        draw.rect(surface, color, self.rect, border_radius=8)
        label = button_font.render(self.text, True, (25, 25, 35))
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class Player(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 60)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms, bones):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[K_a] or keys[K_LEFT]: self.vel_x = -PLAYER_SPEED
        if keys[K_d] or keys[K_RIGHT]: self.vel_x = PLAYER_SPEED
        if (keys[K_SPACE] or keys[K_w] or keys[K_UP]) and self.on_ground:
            self.vel_y = -JUMP_FORCE
            self.on_ground = False

        self.vel_y += GRAVITY

        self.x += self.vel_x
        for p in platforms:
            if self.colliderect(p):
                if self.vel_x > 0:
                    self.right = p.left
                elif self.vel_x < 0:
                    self.left = p.right

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

        global score
        for b in bones:
            if not b.collected and self.colliderect(b):
                b.collected = True
                score += 1

    def draw(self, surface):
        surface.blit(dog_img, (self.x, self.y))


platforms1 = [Rect(0, HEIGHT - 40, WIDTH, 40), Rect(-65, 100, 70, 800), Rect(120, 520, 60, 12), Rect(260, 460, 50, 12),
              Rect(380, 400, 45, 12), Rect(520, 340, 40, 12), Rect(650, 280, 35, 12), Rect(780, 220, 30, 12),
              Rect(880, 160, 25, 12), Rect(1120, 100, 70, 800)]
platforms2 = [Rect(0, HEIGHT - 40, WIDTH, 40), Rect(-65, 100, 70, 800), Rect(60, 520, 90, 12), Rect(180, 480, 70, 12),
              Rect(300, 440, 80, 12), Rect(420, 400, 65, 12), Rect(540, 360, 75, 12), Rect(660, 320, 60, 12),
              Rect(780, 280, 70, 12), Rect(900, 240, 55, 12), Rect(820, 200, 60, 12), Rect(744, 240, 70, 12),
              Rect(460, 280, 65, 12), Rect(280, 500, 80, 12), Rect(1120, 150, 70, 600), Rect(150, 560, 60, 10),
              Rect(350, 520, 50, 10), Rect(520, 500, 60, 10), Rect(620, 420, 50, 10), Rect(740, 390, 45, 10),
              Rect(860, 360, 50, 10), Rect(950, 300, 45, 10), Rect(880, 330, 40, 10), Rect(600, 260, 55, 10),
              Rect(480, 240, 50, 10), Rect(360, 200, 60, 10), Rect(240, 180, 50, 10), Rect(100, 140, 60, 10),
              Rect(200, 120, 70, 10),]
platforms3 = [Rect(40, 520, 160, 16), Rect(260, 500, 80, 14), Rect(380, 460, 60, 14), Rect(300, 400, 40, 12),
              Rect(420, 370, 35, 12), Rect(600, 340, 120, 14), Rect(760, 300, 30, 12), Rect(820, 260, 28, 12),
              Rect(780, 220, 26, 12), Rect(900, 240, 100, 10), Rect(1040, 180, 60, 12), Rect(1120, 150, 70, 600),
              Rect(110, 470, 26, 8), Rect(210, 450, 22, 8), Rect(340, 360, 20, 8), Rect(460, 330, 18, 8),
              Rect(520, 300, 22, 8), Rect(650, 280, 24, 8), Rect(720, 260, 20, 8), Rect(790, 180, 18, 8),
              Rect(840, 160, 18, 8), Rect(960, 200, 22, 8), Rect(1020, 140, 20, 8), Rect(580, 140, 26, 8),
              Rect(420, 120, 24, 8),]
platforms4 = [Rect(0, HEIGHT - 40, WIDTH, 40), Rect(120, 480, 90, 14), Rect(300, 430, 80, 14),
              Rect(500, 380, 70, 14), Rect(700, 330, 60, 14), Rect(880, 280, 55, 14), Rect(650, 220, 60, 14),
              Rect(400, 170, 70, 14)]
platforms5 = [Rect(0, HEIGHT - 40, WIDTH, 40), Rect(-65, 100, 70, 800), Rect(480, 500, 60, 12), Rect(420, 440, 50, 12),
              Rect(520, 380, 45, 12), Rect(400, 320, 40, 12), Rect(540, 260, 35, 12), Rect(380, 200, 30, 12),
              Rect(560, 140, 25, 12), Rect(1120, 120, 70, 600)]

bones1 = [Bone(130, 490), Bone(550, 350)]
bones2 = [Bone(70, 600), Bone(830, 100), Bone(100, 250), Bone(550, 300)]
bones3 = [Bone(50, 490), Bone(510, 250)]
bones4 = [Bone(160, 440), Bone(810, 270)]
bones5 = [Bone(490, 470), Bone(550, 230)]

player = Player(100, 100)
start_btn = Button("START", WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50,)
exit_btn = Button("EXIT", WIDTH // 2 - 80, HEIGHT // 2 + 110, 160, 50)

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if state == MENU:
            if start_btn.clicked(e):
                state = LEVEL1
                score = 0
                for b in bones1 + bones2 + bones3: b.collected = False
            if exit_btn.clicked(e):
                running = False

    if state == MENU:
        if playing_music != "menu":
            mixer.music.load(music_menu)
            mixer.music.play(-1)
            playing_music = "menu"
        screen.blit(menu_bg, (0, 0))
        start_btn.draw(screen)
        exit_btn.draw(screen)
    else:
        if playing_music != "game":
            mixer.music.load(music_game)
            mixer.music.play(-1)
            playing_music = "game"

        if state == LEVEL1:
            screen.blit(back1, (0, 0))
            cur_p, cur_b = platforms1, bones1
            if player.right > WIDTH:
                state, player.x, player.y = LEVEL2, 0, 100
        elif state == LEVEL2:
            screen.blit(back2, (0, 0))
            cur_p, cur_b = platforms2, bones2
            if player.right > WIDTH:
                state, player.x, player.y = LEVEL3, 0, 100
        elif state == LEVEL3:
            screen.blit(back3, (0, 0))
            cur_p, cur_b = platforms3, bones3
            if player.right > WIDTH:
                state, player.x, player.y = MENU, 100, 100
        elif state == LEVEL4:
            screen.blit(back3, (0, 0))
            cur_p, cur_b = platforms4, bones4
            if player.right > WIDTH:
                state, player.x, player.y = MENU, 100, 100
        elif state == LEVEL5:
            screen.blit(back3, (0, 0))
            cur_p, cur_b = platforms5, bones5
            if player.right > WIDTH:
                state, player.x, player.y = MENU, 100, 100

        player.update(cur_p, cur_b)
        for p in cur_p:
            screen.blit(transform.scale(plat_img, (p.width, p.height)), (p.x, p.y))
        for b in cur_b:
            b.draw(screen)
        player.draw(screen)

        txt = score_font.render(f"Bones: {score}", True, WHITE)
        screen.blit(txt, (20, 20))

    display.flip()
    clock.tick(FPS)

pygame.quit()
