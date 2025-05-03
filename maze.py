#создай игру "Лабиринт"!
from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')

background = transform.scale(image.load('background.jpg'), (700, 500))
player = transform.scale(image.load('hero.png'), (100, 100))
enemy = transform.scale(image.load('cyborg.png'), (100, 100))
treasure = transform.scale(image.load('treasure.png'), (100, 100))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')

font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN', True, (255, 215, 0))
lose = font.render('YOU LOSE', True, (255, 0, 0))
clock = time.Clock()
FPS = 60
game = True
finish = False

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - 70:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 500 - 70:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 400:
            self.direction = "right"
        if self.rect.x > 600:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Player('hero.png', 50, 415, 10)
enemy = Enemy('cyborg.png', 400, 350, 7)
treasure = GameSprite('treasure.png', 500, 450, 0)
wall1 = Wall(120, 120, 0, 150, 0, 7, 400)
wall2 = Wall(120, 120, 0, 250, 100, 7, 400)
wall3 = Wall(120, 120, 0, 150, 0, 400, 7)
wall4 = Wall(120, 120, 0, 150, 493, 100, 7)
wall5 = Wall(120, 120, 0, 250, 100, 300, 7)

while game:
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        enemy.update()
        enemy.reset()
        treasure.reset()
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall4) or sprite.collide_rect(player, wall5):
            window.blit(lose, (200, 200))
            finish = True
            kick.play()
        if sprite.collide_rect(player, treasure):
            window.blit(win, (200, 200))
            finish = True
            money.play()
    
    clock.tick(FPS)
    display.update()

    for e in event.get():
        if e.type == QUIT:
            game = False