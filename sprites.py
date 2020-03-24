import pygame
from const import *
import random

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, myBullets, Allsprites):
        pygame.sprite.Sprite.__init__(self)
        self.bullets = myBullets
        self.all_sprites = Allsprites
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        pygame.draw.ellipse(self.image, WHITE, self.rect)

        # self.image.fill(WHITE)
        self.rect.center = (WIDTH // 2, 60)

        # MOTION
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.pos = vec(WIDTH // 2, 60)

        self.ammo_loader = 0

    def isOnFloor(self):
        if self.rect.y == 381:
            return True
        else:
            return False

    def update(self):
        self.ammo_loader += 1
        self.acc = vec(0, 0.9)

        # FLOOR
        # if self.rect.bottom > HEIGHT - 31:
        #     print("coisa")
        #     self.pos.y = HEIGHT - 32
        #     self.vel.y = 0

        if self.pos.y > HEIGHT:
            self.pos.y = - 30

        if self.pos.x > WIDTH:
            self.pos.x = 0

        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.key_pressed = pygame.key.get_pressed()
        if self.key_pressed[pygame.K_LEFT]:
            self.acc.x = -1.5
        if self.key_pressed[pygame.K_RIGHT]:
            self.acc.x = 1.5

        if self.key_pressed[pygame.K_DOWN]:
            if self.ammo_loader > 10:
                self.bullet = Bullet(self.rect.center[0], self.rect.center[1])
                self.bullets.add(self.bullet)
                self.all_sprites.add(self.bullets)
                self.ammo_loader = 0

        # MOTION
        self.acc += self.vel * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 30))
        self.rect = self.image.get_rect()

        self.rect.top = HEIGHT - 30
        self.image.fill(WHITE)


class Plattform(pygame.sprite.Sprite):
    def __init__(self, w=150, h=2):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.kind = type
        self.life = h * 30
        self.speed = LEVEL_CONTROL
        self.counter = 0

    def update(self):

        if self.counter > 80:
            self.rect.y -= self.speed
            if self.rect.y < -30:
                self.rect.y = random.randrange(HEIGHT + 30, HEIGHT + 200, 60)
                self.rect.x = random.randrange(0, WIDTH, 60)
                self.image.fill(WHITE)

            # self.counter *= 1.0001
            if self.life <= 0:

                self.__init__(150, random.randrange(2, 10))
        else:
            self.counter += 1


class Rain:
    class RainDrop1(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.Surface((3, 3))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect_speed = random.randrange(2, 30)
            self.rect.y = HEIGHT - 5

        def update(self):
            self.rect.x += 3

            self.rect.y += self.rect_speed + 4

            if self.rect.y >= HEIGHT:
                self.rect.x = random.randrange(-WIDTH, WIDTH)
                self.rect.y = -100
                self.rect_speed = random.randrange(2, 20)

    class RainDrop2(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.xy = random.randrange(1, 3)
            self.image = pygame.Surface((self.xy, self.xy)).convert_alpha()
            self.rect = pygame.draw.ellipse(self.image, [0, 0, 0], [0, 0, 2, 2])
            self.rect.x = random.randrange(-WIDTH, WIDTH)
            self.rect.y = random.randrange(-HEIGHT, HEIGHT)
            self.rect_speed = random.randrange(5, 10)
            self.color = WHITE

            self.speed_up = False

        def update(self):
            if self.speed_up:
                self.rect.x += 20
            else:
                self.rect.x += 7

            self.rect.y += self.rect_speed

            if (self.rect.x > WIDTH + 2) or (self.rect.y > HEIGHT + 2):
                self.rect.x = random.randrange(-WIDTH, WIDTH)
                self.rect.y = random.randrange(5, 10)
                self.__init__()

            self.image.fill(self.color)

    class RainDrop3(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.counter = 0
            self.image = pygame.Surface((2, 2))
            self.image.fill(grey)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(-WIDTH, WIDTH)
            self.rect_speed = random.randrange(10, 20)
            self.rect.y = random.randrange(-300, -100)

        def update(self):
            self.counter += 1
            if self.counter > 30:
                self.kill()
            if self.rect.y >= HEIGHT - 30:
                self.rect.y = HEIGHT - 30
            else:
                self.rect.x += 3
                self.rect.y += self.rect_speed + 6


def match(mouse_x, mouse_y, width, height):
    '''

    :author: Isaque Melo
    :param mouse_x: Mouse X variable (int - float)
    :param mouse_y: Mouse Y variable (int - float)
    :param width: Window width
    :param height: Window height
    :return: (r, g, b)

    '''
    r = int((mouse_x / width) * 255) % 255
    g = int((mouse_y / height) * 255) % 255
    b = int((((r + g) / width + height) % 255))

    if r > 150:
        r -= 50

    return mod(r), mod(g), b


def mod(n):
    if n > 0:
        return n
    else:
        return n * -1


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, RED, self.rect)


class Speed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 80
        self.rect.y = 100
        self.colour = (0, 0, 0)

    def update(self):
        self.image.fill(self.colour)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.image.fill(WHITE)

    def update(self):
        self.rect.y += 15
        if self.rect.y > HEIGHT:
            self.kill()
