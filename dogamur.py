import pygame
from pygame import *

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 700
FPS = 60
GRAVITY = 0.9
PLAYER_SPEED = 6
JUMP_FORCE = 20

WHITE = (240, 240, 240)
GRAY = (180, 180, 180)
HOVER = (220, 220, 220)
GREEN = (50, 200, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dog Amur")
clock = pygame.time.Clock()

menu_bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))
# Завантаження фону для історії
try:
    history_bg = transform.scale(image.load("history.jpg"), (WIDTH, HEIGHT))
except:
    history_bg = menu_bg  # Якщо картинки немає, буде фон меню

back1 = transform.scale(image.load("back1.jpg"), (WIDTH, HEIGHT))
back2 = transform.scale(image.load("back2.jpg"), (WIDTH, HEIGHT))
back3 = transform.scale(image.load("back3.jpg"), (WIDTH, HEIGHT))
back4 = transform.scale(image.load("back4.jpg"), (WIDTH, HEIGHT))
back5 = transform.scale(image.load("back5.jpg"), (WIDTH, HEIGHT))
dog_img = transform.scale(image.load("dog.png"), (110, 120))
plat_img = image.load("platform.png")
bone_img = image.load("bone2.png")
end_img = image.load("end.jpg")

hill_img = transform.scale(image.load("hill.png"), (120, 350))

music_menu = "menu_music.mp3"
music_game = "game_music.mp3"

step = pygame.mixer.Sound("elegant-high-heels-with-an-empty-reverb.mp3")
jump = pygame.mixer.Sound("elegant-high-heels-with-an-empty-reverb.mp3")
prizem = pygame.mixer.Sound("elegant-high-heels-with-an-empty-reverb.mp3")
# Завантаження гавкоту
dog_bark = pygame.mixer.Sound("dog-bark-15.mp3")

pygame.mixer.music.load(music_menu)
pygame.mixer.music.play(-1)
playing_music = "menu"

button_font = pygame.font.SysFont("comicsansms", 28)
story_font = pygame.font.SysFont("comicsansms", 24)
score_font = pygame.font.SysFont("comicsansms", 36, bold=True)

MENU = "menu"
STORY = "story"
LEVEL1 = "level1"
LEVEL2 = "level2"
LEVEL3 = "level3"
LEVEL4 = "level4"
LEVEL5 = "level5"
END = "end"
state = MENU
score = 0

story_text_lines = [
    "Прривітусики мою любі друзі. Не так давно сталася зі мною одна пригода....",
    "Я загубився. Але ж я розумнй пес і розумів як потрібно дійти додому!",
    "Тому давайте я ще раз переживу цю історію з вами!"
]
current_line = 0
current_char = 0
text_timer = 5
char_speed = 0


class Hill(Rect):
    def __init__(self, x, y):
        super().__init__(x, y, hill_img.get_width(), hill_img.get_height())
        self.image = hill_img

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


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

    def update(self, platforms, hills, bones):
        keys = pygame.key.get_pressed()

        self.vel_x = 0
        if keys[K_a] or keys[K_LEFT]:
            self.vel_x = -PLAYER_SPEED
        if keys[K_d] or keys[K_RIGHT]:
            self.vel_x = PLAYER_SPEED

        if (keys[K_SPACE] or keys[K_w] or keys[K_UP]) and self.on_ground:
            self.vel_y = -JUMP_FORCE
            pygame.mixer.Channel(1).play(jump)
            self.on_ground = False

        walk_channel = pygame.mixer.Channel(0)
        if abs(self.vel_x) > 0 and self.on_ground:
            if not walk_channel.get_busy():
                walk_channel.play(step, loops=-1)
        else:
            walk_channel.stop()

        self.is_jumping = False

        self.vel_y += GRAVITY

        self.x += self.vel_x
        for p in platforms + hills:
            if self.colliderect(p):
                if self.vel_x > 0:
                    self.right = p.left
                elif self.vel_x < 0:
                    self.left = p.right

        self.y += self.vel_y
        self.on_ground = False

        for p in platforms + hills:
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
        surface.blit(dog_img, (self.x - 35, self.y - 60))


floor = Rect(-2000, HEIGHT - 40, WIDTH * 5, 200)

platforms1 = [floor, Rect(120, 520, 80, 15), Rect(260, 460, 70, 15),
              Rect(380, 400, 65, 15), Rect(520, 340, 60, 15), Rect(650, 280, 55, 15), Rect(780, 220, 50, 15),
              Rect(880, 160, 45, 15)]
hills1 = [Hill(1120, 310)]
bones1 = [Bone(130, 475), Bone(530, 295)]

platforms2 = [floor, Rect(60, 520, 110, 15), Rect(180, 480, 90, 15),
              Rect(300, 440, 100, 15), Rect(420, 400, 85, 15), Rect(540, 360, 95, 15), Rect(660, 320, 80, 15),
              Rect(780, 280, 90, 15), Rect(900, 240, 75, 15), Rect(820, 200, 80, 15), Rect(744, 240, 90, 15),
              Rect(460, 280, 85, 15), Rect(280, 500, 100, 15), Rect(150, 560, 80, 15),
              Rect(350, 520, 70, 15), Rect(520, 500, 80, 15), Rect(620, 420, 70, 15), Rect(740, 390, 65, 15),
              Rect(860, 360, 70, 15), Rect(950, 300, 65, 15), Rect(880, 330, 60, 15), Rect(600, 260, 75, 15),
              Rect(480, 240, 70, 15), Rect(360, 200, 80, 15), Rect(240, 180, 70, 15), Rect(100, 140, 80, 15),
              Rect(200, 120, 90, 15), ]
hills2 = [Hill(1120, 310)]
bones2 = [Bone(70, 560), Bone(830, 155), Bone(110, 475), Bone(550, 315)]

platforms3 = [floor, Rect(40, 520, 180, 16), Rect(260, 500, 100, 14), Rect(380, 460, 80, 14), Rect(300, 400, 60, 12),
              Rect(420, 370, 55, 12), Rect(600, 340, 140, 14), Rect(760, 300, 50, 12), Rect(820, 260, 48, 12),
              Rect(780, 220, 46, 12), Rect(900, 240, 120, 10), Rect(1040, 180, 80, 12),
              Rect(110, 470, 46, 15), Rect(210, 450, 42, 15), Rect(340, 360, 40, 15), Rect(460, 330, 38, 15),
              Rect(520, 300, 42, 15), Rect(650, 280, 44, 15), Rect(720, 260, 40, 15), Rect(790, 180, 38, 15),
              Rect(840, 160, 38, 15), Rect(960, 200, 42, 15), Rect(1020, 140, 40, 15), Rect(580, 140, 46, 15), ]
hills3 = [Hill(1120, 310)]
bones3 = [Bone(50, 475), Bone(620, 295)]

hills4 = []
platforms4 = [floor, Rect(80, 520, 140, 16), Rect(150, 480, 130, 16),
              Rect(220, 440, 120, 16), Rect(300, 400, 110, 14), Rect(380, 360, 100, 14), Rect(460, 320, 100, 14),
              Rect(540, 280, 100, 14), Rect(620, 240, 100, 14), Rect(700, 210, 100, 14), Rect(780, 180, 100, 14),
              Rect(860, 150, 100, 14), Rect(940, 120, 220, 20), ]
bones4 = [Bone(180, 435), Bone(820, 135)]

platforms5 = [
    floor,
    Rect(450, 550, 100, 15),
    Rect(600, 470, 90, 15),
    Rect(450, 390, 80, 15),
    Rect(600, 310, 70, 15),
    Rect(450, 230, 60, 15),
    Rect(580, 150, 300, 15)
]
hills5 = [Hill(-65, 310), Hill(1120, 310)]
bones5 = [Bone(490, 455), Bone(560, 185)]

player = Player(100, 100)
start_btn = Button("START", WIDTH // 2 - 80, HEIGHT // 2 + 40, 160, 50, )
exit_btn = Button("EXIT", WIDTH // 2 - 80, HEIGHT // 2 + 110, 160, 50)
next_btn = Button("NEXT", WIDTH - 180, HEIGHT - 80, 150, 50)

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if state == MENU:
            if start_btn.clicked(e):
                state = STORY
                # Скидання параметрів друку тексту
                current_line = 0
                current_char = 0
                text_timer = 0
                # Граємо гавкіт один раз при переході
                dog_bark.play()
            if exit_btn.clicked(e):
                running = False
        elif state == STORY:
            if next_btn.clicked(e):
                state = LEVEL1
                score = 0
                for b in bones1 + bones2 + bones3 + bones4 + bones5: b.collected = False

    if state == MENU:
        if playing_music != "menu":
            mixer.music.load(music_menu)
            mixer.music.play(-1)
            mixer.music.set_volume(0.9)
            playing_music = "menu"
        screen.blit(menu_bg, (0, 0))
        start_btn.draw(screen)
        exit_btn.draw(screen)

    elif state == STORY:
        screen.blit(history_bg, (0, 0))

        s = Surface((WIDTH, 200))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        screen.blit(s, (0, HEIGHT - 200))

        # Ефект друкарської машинки
        text_timer += 1
        if text_timer >= char_speed:
            text_timer = 0
            if current_line < len(story_text_lines):
                if current_char < len(story_text_lines[current_line]):
                    current_char += 1
                elif current_line < len(story_text_lines) - 1:
                    current_line += 1
                    current_char = 0

        # Малювання тексту
        y_offset = HEIGHT - 150
        for i in range(current_line + 1):
            line_to_draw = story_text_lines[i]
            if i == current_line:
                line_to_draw = line_to_draw[:current_char]

            rendered_text = story_font.render(line_to_draw, True, WHITE)
            screen.blit(rendered_text, (50, y_offset + i * 50))

        # Кнопка NEXT з'являється лише коли весь текст надруковано
        if current_line == len(story_text_lines) - 1 and current_char == len(story_text_lines[-1]):
            next_btn.draw(screen)

    elif state == END:
        if playing_music != "menu":
            mixer.music.load(music_menu)
            mixer.music.play(-1)
            mixer.music.set_volume(0.9)
            playing_music = "menu"

        mixer.Channel(0).stop()
        mixer.Channel(1).stop()

        screen.blit(end_img, (0, 0))

    else:
        if playing_music != "game":
            mixer.music.load(music_game)
            mixer.music.play(-1)
            playing_music = "game"
            mixer.music.set_volume(0.3)

        if state == LEVEL1:
            screen.blit(back1, (0, 0))
            cur_p, cur_h, cur_b = platforms1, hills1, bones1
            if player.right > WIDTH:
                state, player.x, player.y = LEVEL2, 0, 100
        elif state == LEVEL2:
            screen.blit(back2, (0, 0))
            cur_p, cur_h, cur_b = platforms2, hills2, bones2
            if player.right > WIDTH:
                state, player.x, player.y = LEVEL3, 0, 100
        elif state == LEVEL3:
            screen.blit(back3, (0, 0))
            cur_p, cur_h, cur_b = platforms3, hills3, bones3
            if player.right > WIDTH:
                state, player.x, player.y = LEVEL4, 100, 100
        elif state == LEVEL4:
            screen.blit(back4, (0, 0))
            cur_p, cur_h, cur_b = platforms4, hills4, bones4
            if player.right > WIDTH:
                state, player.x, player.y = LEVEL5, 100, 100
        elif state == LEVEL5:
            screen.blit(back5, (0, 0))
            cur_p, cur_h, cur_b = platforms5, hills5, bones5
            if player.right > WIDTH:
                cur_p.clear()
                cur_b.clear()
                cur_h.clear()
                state = END

        player.update(cur_p, cur_h, cur_b)

        for p in cur_p:
            if p == floor:
                draw.rect(screen, GREEN, p)
            else:
                screen.blit(transform.scale(plat_img, (p.width, p.height)), (p.x, p.y))

        for h in cur_h:
            h.draw(screen)
        for b in cur_b:
            b.draw(screen)
        player.draw(screen)

        txt = score_font.render(f"Bones: {score}", True, WHITE)
        screen.blit(txt, (20, 20))

    display.flip()
    clock.tick(FPS)

pygame.quit()
