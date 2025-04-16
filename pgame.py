import pygame
from Charactor import Charactor
pygame.init()

# game window
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL

# CREATE GAME WINDOW
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Change_name_ofGAME')

clock = pygame.time.Clock()
FPS = 60

#load images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

# function for drawing background

def draw_bg():
    screen.blit(background_img, (0,0))

def draw_panel():
    screen.blit(panel_img, (0, screen.get_height() - BOTTOM_PANEL))
# Hero class

knight = Charactor(200, 260, 'Knight', 30,10, 3)
bandit1 = Charactor(400, 270, 'Bandit', 20,6, 1)
Boss1 = Charactor(700, 270, 'Bandit', 20,6, 1)

enemy_list = []
enemy_list.append(bandit1)
#game loop
run = True
while run:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    draw_bg()
    draw_panel()
    # draw fighters
    knight.draw(screen)
    bandit1.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()