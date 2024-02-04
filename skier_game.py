import os
import sys

import pygame
import random

skier_images = ["data/skier_down.png", "data/skier_right.png", "data/skier_right1.png",
                "data/skier_left1.png", "data/skier_left.png"]


class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/skier_down.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = [800, 100]
        self.angle = 0

    def turn(self, direction):
        self.angle = self.angle + direction
        if self.angle < -2:
            self.angle = -2
        if self.angle > 2:
            self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed_skier = [self.angle, (6 - abs(self.angle) * 2) + boost]
        return speed_skier

    def move(self, speed_skier):
        self.rect.centerx = self.rect.centerx + speed_skier[0]
        if self.rect.centerx < 50:
            self.rect.centerx = 50
        if self.rect.centerx > 1550:
            self.rect.centerx = 1550


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type_obst):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type_obst
        self.passed = False

    def update(self):
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


def create_map():
    global obstacles
    locations = []
    for i in range(11):
        row = random.randint(0, 10)
        col = random.randint(0, 10)
        location = [col * 150 + 60, row * 150 + 60 + 1700]
        if not (location in locations):
            locations.append(location)
            type_obstacle = random.choice(["tree", "flag"])
            if type_obstacle == "tree":
                img = "data/tree.png"
            elif type_obstacle == "flag":
                img = "data/flag.png"
            obstacle = ObstacleClass(img, location, type_obstacle)
            obstacles.add(obstacle)


def animate():
    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode([1600, 900])
pygame.display.set_caption('Skier Game')
clock = pygame.time.Clock()
boost = 0.5
speed = [0, 6]
obstacles = pygame.sprite.Group()
skier = SkierClass()
map_position = 0
points = 0
create_map()
font = pygame.font.Font(None, 50)

FPS = 60


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Skier Game"]

    fon = pygame.transform.scale(load_image('fon.png'), (1600, 900))
    screen.blit(fon, (0, 0))

    font_name = pygame.font.Font(None, 80)
    text_coord = 150
    for line in intro_text:
        string_rendered = font_name.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    run = True
    x_quit = 800
    y_quit = 400
    x_run = 800
    y_run = 200
    while run:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                terminate()

            (mouse_posx, mouse_posy) = pygame.mouse.get_pos()
            pressed = pygame.mouse.get_pressed()
            button_quit = pygame.transform.scale(load_image("quit.png"), (300, 150))
            screen.blit(button_quit, (800, 400))
            button_run = pygame.transform.scale(load_image("start.png"), (300, 150))
            screen.blit(button_run, (800, 200))
            if x_quit < mouse_posx < x_quit + 300 and y_quit < mouse_posy < y_quit + 150 and pressed[0]:
                terminate()
            if x_run < mouse_posx < x_run + 300 and y_run < mouse_posy < y_run + 150 and pressed[0]:
                run = False

        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    bg_img = load_image("gameover.png")
    bg_img = pygame.transform.scale(bg_img, (1600, 900))
    x_pos = 0
    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(bg_img, (x_pos, 0))
        screen.blit(bg_img, (1600 + x_pos, 0))
        if x_pos == 1600:
            screen.blit(bg_img, (1600 + x_pos, 0))
            x_pos = 0
        x_pos -= 1
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                terminate()
            elif event1.type == pygame.KEYDOWN or \
                    event1.type == pygame.MOUSEBUTTONDOWN:
                run = False
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:
                speed = skier.turn(1)
    skier.move(speed)
    map_position += speed[1]

    if map_position >= 1600:
        create_map()
        map_position = 1

    hit = pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        if hit[0].type == "tree" and not hit[0].passed:
            boost += 0.25
            points = points - 30
            skier.image = pygame.image.load("data/skier_crash.png")
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load("data/skier_down.png")
            if skier.angle == 0:
                skier.image = pygame.image.load("data/skier_down.png")
                skier.angle = 0
            elif skier.angle == -1:
                skier.image = pygame.image.load("data/skier_left.png")
                skier.angle = -1
            elif skier.angle == 1:
                skier.image = pygame.image.load("data/skier_right.png")
                skier.angle = 1
            elif skier.angle == -2:
                skier.image = pygame.image.load("data/skier_left1.png")
                skier.angle = -2
            elif skier.angle == 2:
                skier.image = pygame.image.load("data/skier_right1.png")
                skier.angle = 2
            speed[1] += boost
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:
            points += 10
            speed[1] -= boost
            hit[0].kill()
        elif points < 0:
            end_screen()
            terminate()

    obstacles.update()
    score_text = font.render("Score: " + str(points), 1, (0, 0, 0))
    animate()

pygame.quit()
