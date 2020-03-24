import pygame as pg
from sprites import *
from const import *

pygame.init()
width = 800
height = 500
fps = 60
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.points = 1350
        self.LEVEL_CONTROL = 8

        # PRINTS MAP
        # for i in range(len(self.map_matriz)):
        #     print(self.map_matriz[i])

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text, x, y, color, size=80):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf, TextRect = self.text_objects(str(text), largeText, color)
        TextRect.x, TextRect.y = (x, y)
        self.screen.blit(TextSurf, TextRect)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.solid = pg.sprite.Group()
        self.plat_g = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        self.player = Player(self.bullets, self.all_sprites)
        self.floor = Floor()
        self.bonus = Bonus()

        for i in range(PLATTAFORM_GENERATE):
            self.plattform = Plattform()
            self.plat_g.add(self.plattform)

        self.solid.add(self.floor)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.plat_g)
        self.all_sprites.add(self.bullets)

        for rain in range(300):
            self.drop_2 = Rain.RainDrop2()
            self.particles.add(self.drop_2)

        self.all_sprites.add(self.particles)
        # self.all_sprites.add(self.bonus)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        for i in self.particles:
            if pygame.sprite.spritecollide(i, self.plat_g, False):
                i.color = BLUE

        self.LEVEL_CONTROL += self.points + 0.01

        if self.points > 1400:
            for i in self.particles:
                i.speed_up = True

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    if self.player.rect.y > (HEIGHT // 2) - 100:
                        self.player.vel.y = -17

        if self.points < 0:
            self.playing = False
            self.running = False

    def draw(self):

        # Game Loop - draw
        self.screen.fill(match(self.player.rect.x, self.player.rect.y, WIDTH, HEIGHT))
        self.message_display("MyRain - Isaque Melo", 100, 50, WHITE, 30)

        # self.screen.fill(BLUE_B)

        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display

        # TEXTES
        self.points += 0.1

        def missing(string):
            falta = False
            if string < 0:
                myString = str(int(string) * -1)
                falta = True
            else:
                myString = str(int(string))

            amnt = (4 - len(myString)) if not falta else (4 - len(myString))
            return ('-' if falta else '+') + str(('0' * amnt) + myString)

        self.message_display(missing(self.points), 100, 100, WHITE, 82 + LEVEL_CONTROL)

        # print(self.player.vel.x + self.player.vel.y)
        self.isPrinting = False

        if 70 > (mod(self.player.vel.x + self.player.vel.y)) > 40:
            self.message_display("NICE SPEED", 100, 190, WHITE, 50)
            self.points += mod(self.player.vel.x + self.player.vel.y) % 5
            self.message_display("+", 420, 190, WHITE, 40)
            self.message_display(str(int(mod(self.player.vel.x + self.player.vel.y) % 10)), 450, 195, WHITE, 40)

            self.isPrinting = True
        elif 75 > (mod(self.player.vel.x + self.player.vel.y)) >= 70:
            self.message_display("FREAKIN'", 100, 190, WHITE, 80)
            self.points += mod(self.player.vel.x + self.player.vel.y) % 10
            self.message_display("+", 500, 190, WHITE, 70)
            self.message_display(str(int(mod(self.player.vel.x + self.player.vel.y) % 15)), 560, 190, WHITE, 80)
            self.isPrinting = True

        elif (mod(self.player.vel.x + self.player.vel.y)) >= 75:
            self.message_display("TERRIFIC", 100, 190, WHITE, 90)
            self.points += mod(self.player.vel.x + self.player.vel.y) % 15
            self.message_display("+", 550, 190, WHITE, 80)
            self.message_display(str(int(mod(self.player.vel.x + self.player.vel.y) % 20)), 600, 190, WHITE, 90)
            self.isPrinting = True

        collision_plattaform = pygame.sprite.spritecollide(self.player, self.plat_g, False)

        if collision_plattaform and self.player.pos.y >= collision_plattaform[0].rect.top:
            self.player.pos.y = collision_plattaform[0].rect.y - 2
            self.player.vel.y = 0
            self.points -= LEVEL_CONTROL

            if (mod(self.player.vel.x + self.player.vel.y)) >= 60:
                self.points = self.points - mod(self.player.vel.x + self.player.vel.y) - self.points * 0.2
                print("genius ")
            if self.isPrinting:
                self.message_display("- " + str(int(collision_plattaform[0].life)), 100, 250, WHITE, 60)
            else:
                self.message_display("- " + str(int(collision_plattaform[0].life)), 100, 180, WHITE, 60)
            collision_plattaform[0].life -= self.points * 0.01

        self.isPrinting = False

        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
