import pygame
import os

pygame.init()



# Loading images
REDENEMY = pygame.image.load(os.path.join("graphics", "redenemy.png"))
GREENENEMY = pygame.image.load(os.path.join("graphics", "greenenemy.png"))
BLUEENEMY = pygame.image.load(os.path.join("graphics", "blueenemy.png"))

BACKGROUND_IMAGE = pygame.image.load(os.path.join("graphics", "background_menu.jpg"))

REDENEMY = pygame.transform.scale(REDENEMY, (30,30))
BLUEENEMY = pygame.transform.scale(BLUEENEMY, (30,30))
GREENENEMY = pygame.transform.scale(GREENENEMY, (30,30))

#Player's spaceship
MAINSPACESHIP = pygame.image.load(os.path.join("graphics", "MAINSPACESHIP_new.png"))
MAINSPACESHIP = pygame.transform.scale(MAINSPACESHIP, (75,75))
#Lasers
RED_LASER = pygame.image.load(os.path.join("graphics", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("graphics", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("graphics", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("graphics", "pixel_laser_yellow.png"))

#background image
BG = pygame.image.load(os.path.join("graphics", "bg.jpg"))