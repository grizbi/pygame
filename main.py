

import sys

import pygame
import os
import time
import random
import game_module as gm

pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Battle")




window_open = True
FPS = 60
main_font = pygame.font.SysFont("Helvetica", 50)
menu_font = pygame.font.SysFont("comicsansms", 80)
enemies = []
wave_length = 0
clock = pygame.time.Clock()
level = 0
click = False



class SpaceShip:
    def __init__(self, x, y, health=100):
        self.level = 0
        self.lives = 10
        self.x = x
        self.y = y
        self.spaceship_img = None
        self.shot_img = None
        self.velocity = 5
        self.cool_down_shot = 0
        self.shots = []


    def create_shot(self, image):
        if self.cool_down_shot==0:
            shot = Shot(self.x, self.y, image)
            self.shots.append(shot)
            self.cool_down_shot=30


    def get_width(self):
        return self.spaceship_img.get_width()


    def get_height(self):
        return self.spaceship_img.get_height()

class Shot():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.velocity = 5
        self.image = image
        self.laser_rect = self.image.get_rect()
        self.laser_rect.x = x
        self.laser_rect.y = y


    def collision(self, obj2):
        return self.laser_rect.colliderect(obj2)

    def collision_with_player(self, obj2):
        return self.laser_rect.colliderect(obj2)





class Player(SpaceShip):
    def __init__(self, x, y, health=100):
        super(Player, self).__init__(x, y)
        self.spaceship_img = gm.MAINSPACESHIP
        self.rect_of_players_spaceship = self.spaceship_img.get_rect()
        self.laser_img = gm.YELLOW_LASER
        self.rect_of_players_laser = self.laser_img.get_rect()
        self.rect_of_players_laser.y = y
        self.health = health
        self.rect_of_players_spaceship.x = x
        self.rect_of_players_spaceship.y = y
        self.lost = False
        self.score = 0


    def draw(self):
        lives_text = main_font.render(f"Lives: {self.lives}", 1, (255,255,255))
        level_text = main_font.render(f"Level: {self.level}", 1, (255,255,255))
        health = main_font.render(f"Health: {self.health}", 1, (255, 0, 0))
        score = main_font.render(f"Score: {self.score}", 1, (255, 255, 255))
        final_score = main_font.render(f"Final Score: {self.score}", 1, (255, 255, 255))
        WIN.blit(lives_text, (10, 10))
        WIN.blit(level_text, (WIDTH - 170, 10))
        WIN.blit(health, (10, HEIGHT-70))
        WIN.blit(score, (10, 80))
        WIN.blit(self.spaceship_img, (self.rect_of_players_spaceship.x, self.rect_of_players_spaceship.y))
        if self.lives<=0 or self.health<=0:
            self.lost = True
            lost_message = main_font.render(f"You've just lost the game", 1, (255,255,255))
            WIN.blit(lost_message, (WIDTH/2-lost_message.get_width()/2, 350))
            WIN.blit(final_score, (WIDTH / 2 - final_score.get_width() / 2, 500))
            WIN.blit(self.spaceship_img, (self.rect_of_players_spaceship.x, self.rect_of_players_spaceship.y))
            pygame.mixer.music.load('graphics\\Explosion.mp3')
            pygame.mixer.music.play(0)
        for shot in self.shots:
            WIN.blit(self.laser_img, (shot.laser_rect.x, shot.laser_rect.y))



    def get_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect_of_players_spaceship.x+self.velocity +self.get_width()<WIDTH:
            self.rect_of_players_spaceship.x+=self.velocity
        if keys[pygame.K_LEFT] and self.rect_of_players_spaceship.x-self.velocity>0:
            self.rect_of_players_spaceship.x-=self.velocity
        if keys[pygame.K_UP] and self.rect_of_players_spaceship.y-self.velocity>0:
            self.rect_of_players_spaceship.y-=self.velocity
        if keys[pygame.K_DOWN] and self.rect_of_players_spaceship.y+self.velocity+self.get_height()<HEIGHT:
            self.rect_of_players_spaceship.y+=self.velocity
        if keys[pygame.K_SPACE]:
            self.create_shot(self.laser_img)

        for enemy in enemies:
            if enemy.rect_of_enemy.colliderect(spaceship1.rect_of_players_spaceship): #players spaceship collision with enemy
                spaceship1.health = 0


    def move_shot(self):
        for shot in self.shots:
            shot.laser_rect.y-=shot.velocity
            if shot.laser_rect.y<0:
                self.shots.remove(shot)
            else:
                for enemy in enemies:
                    if shot.collision(enemy.rect_of_enemy): #players shot collision with enemy spaceship
                        self.score+=10
                        enemies.remove(enemy)
                        if shot in self.shots:
                            self.shots.remove(shot)

    def create_shot(self, image):
        if self.cool_down_shot==0:
            shot = Shot(self.rect_of_players_spaceship.x+self.rect_of_players_spaceship.width/2-image.get_width()/2, self.rect_of_players_spaceship.y, image)
            self.shots.append(shot)
            self.cool_down_shot=30
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.load('graphics\\laser_sound.mp3')
            pygame.mixer.music.play(0)





class EnemySpaceShip(SpaceShip):
    COLORS = {
        "red": (gm.REDENEMY, gm.RED_LASER),
        "blue": (gm.BLUEENEMY, gm.BLUE_LASER),
        "green": (gm.GREENENEMY, gm.GREEN_LASER)

    }

    def __init__(self, x, y, color,  health = 100):
        super(EnemySpaceShip, self).__init__(x, y)
        self.spaceship_img, self.spaceship_laser_img = self.COLORS[color]
        self.rect_of_enemy = self.spaceship_img.get_rect()
        self.rect_of_enemy_laser = self.spaceship_laser_img.get_rect()
        self.rect_of_enemy.x = x
        self.rect_of_enemy.y = y
        self.rect_of_enemy_laser.x = x
        self.rect_of_enemy_laser.y = y
        self.velocity = 1.5



    def draw(self):
        WIN.blit(self.spaceship_img, (self.rect_of_enemy.x, self.rect_of_enemy.y))
        for shot in self.shots:
            WIN.blit(self.spaceship_laser_img, (shot.laser_rect.x, shot.laser_rect.y))


    def move(self):
        self.rect_of_enemy.y+=self.velocity




    def move_shot(self):
        for shot in self.shots:
            shot.laser_rect.y+=shot.velocity
            if shot.laser_rect.y > HEIGHT:
                self.shots.remove(shot)
            if shot.collision_with_player(spaceship1.rect_of_players_spaceship):
                spaceship1.health-=20
                self.shots.remove(shot)

    def create_shot(self):
        shot = Shot(self.rect_of_enemy.x+self.rect_of_enemy.width/2-self.spaceship_laser_img.get_width()/2, self.rect_of_enemy.y, self.spaceship_laser_img)
        self.shots.append(shot)




spaceship1 = Player(WIDTH/2-gm.MAINSPACESHIP.get_width()/2, 650)



def mainmenu():
    global window_open, FPS, click
    button1_text = menu_font.render("Start Game", 1, (0, 0, 0))
    button2_text = menu_font.render("Exit", 1, (0, 0, 0))

    while window_open:
        clock.tick(FPS)
        WIN.blit(gm.BACKGROUND_IMAGE, (0, 0))
        mx, my = pygame.mouse.get_pos()
        button1 = pygame.Rect(WIDTH/2-225, 100, 450, 100)
        button2 = pygame.Rect(WIDTH/2-225, 300, 450, 100)
        pygame.draw.rect(WIN, (165, 0, 0), button1)
        pygame.draw.rect(WIN, (165, 0, 0), button2)
        WIN.blit(button1_text, (button1.x, button1.y))
        WIN.blit(button2_text, (button2.x+button2.width/3, button2.y))
        if button1.collidepoint((mx, my)):
            if click:
                loop_game()
        if button2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()



def loop_game():
    global window_open, wave_length
    while window_open:
        clock.tick(FPS)
        WIN.blit(gm.BG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_open = False
                window_open = pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    window_open = False
                    pygame.quit()
                    sys.exit(0)

        if spaceship1.lost==False:
            if len(enemies)==0:
                spaceship1.level+=1
                wave_length+=2
                for x in range(wave_length):
                    enemy_createad = EnemySpaceShip(random.randrange(50,WIDTH-100),random.randrange(0,100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy_createad)
        elif spaceship1.lost:
            start_time = time.time()
            while(time.time()-start_time<2.0):
                continue
            window_open = False

        for enemy in enemies:
            enemy.move()
            enemy.draw()

            if enemy.rect_of_enemy.y>HEIGHT:
                spaceship1.lives-=1
                enemies.remove(enemy)
            if random.randrange(0, 4*60) == 1:
                enemy.create_shot()
            enemy.move_shot()

        spaceship1.get_event()
        spaceship1.move_shot()
        spaceship1.draw()
        if(spaceship1.cool_down_shot):
            spaceship1.cool_down_shot-=1
        pygame.display.update()

mainmenu()
