import pygame
import time
import random
import os

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Sbooter Test")

main_font = pygame.font.SysFont("comicsans",50)
lost_font = pygame.font.SysFont("comicsans", 60)


RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

class Ship:
    COOLDOWN = 15
    def __init__(self,x ,y, vel, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.vel = vel
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, WIN):
        WIN.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(WIN)

    def move_lasers(self,vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    def cooldown (self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self,x,y,vel, health = 100):
        super().__init__(x,y,vel,health = 100)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self,WIN):
        super().draw(WIN)
        self.health_bar(WIN)
    def health_bar(self,WIN):
        pygame.draw.rect(WIN, (255,0,0),(self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width(), 10))
        pygame.draw.rect(WIN, (0, 255, 0),
                         (self.x, self. y + self.ship_img.get_height() + 10,
                          self.ship_img.get_width() * (self.health/self.max_health), 10))
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    def __init__(self,x,y,vel,color,health = 100):
        super(Enemy, self).__init__(x,y,vel,health= 100)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self):
        self.y += self.vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser:
    def __init__(self,x,y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,WIN):
        WIN.blit(self.img,(self.x, self.y))
    def move(self, vel):
        self.y += vel
    def off_screen(self, height):
        return not(self.y <= height and self.y >=0)
    def collision(self,obj):
        return collide(self, obj)


def collide (obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x, offset_y)) != None


def main():
    run = True
    FPS = 30
    level = 0
    lives = 5

    enemies = []
    wave_length = 5
    print(len(enemies))

    lost = False
    lost_count = 0

    player = Player(300, 640, 10 )

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(bg,(0,0))

        lives_label = main_font.render(f'Lives: {lives}',1, (255,255,255))
        level_lable = main_font.render(f'Level: {level}',1, (255,255,255))

        WIN.blit(lives_label, (10,10))
        WIN.blit(level_lable,(WIDTH - level_lable.get_width() - 10,10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_lable = lost_font.render("You lost!",1,(255,255,255))
            WIN.blit(lost_lable,(WIDTH/2 - lost_lable.get_width()/2, HEIGHT/2 - lost_lable.get_height()/2))
        pygame.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(round(-(2000*(level/3))), -100),
                                               random.randrange(level,level + 1),
                                               random.choice(["red","blue","green"]))
                enemies.append(enemy)
        if lives <= 0  or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
           if lost_count> FPS*5:
               run = False
           else:
               continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x > 0: #left
            player.x -= player.vel
        if keys[pygame.K_d] and player.x  < WIDTH - player.get_width() : # right
            player.x += player.vel
        if keys[pygame.K_w] and player.y  > 0 : # up
            player.y -= player.vel
        if keys[pygame.K_s] and player.y  < HEIGHT - player.get_height()-20 : #down
            player.y += player.vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_lasers(enemy.vel + 5, player)
            if random.randrange(0, round(10/level) * 120) == 1 :
                enemy.shoot()
                enemy.move_lasers(enemy.vel + 5, player)
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-(player.vel + 7), enemies)



def main_menu():
    title_font = pygame.font.SysFont('comicsans', 70)
    run = True
    while run:
        WIN.blit(bg, (0,0))
        title_label = title_font.render('Press mouse to begin...',1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2  - title_label.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()