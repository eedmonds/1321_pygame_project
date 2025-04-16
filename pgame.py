import pygame
from Charactor import Charactor
from HealthBar import HealthBar
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

# define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# function for drawing background

def draw_text(text, font, text_col, x, y):
    img = font.render(text,True, text_col)
    screen.blit(img,(x,y))

def draw_bg():
    screen.blit(background_img, (0,0))

def draw_panel():
    screen.blit(panel_img, (0, screen.get_height() - BOTTOM_PANEL))
    #show stats for Charactors
    draw_text(f'{knight.name} HP: {knight.hp}',font, HealthBar.red, 100, SCREEN_HEIGHT-BOTTOM_PANEL +10)
    for count, i in enumerate(enemy_list):
        draw_text(f'{i.name} HP: {i.hp}', font, HealthBar.red, 550, (SCREEN_HEIGHT - BOTTOM_PANEL + 10) + count * 60)



knight = Charactor(200, 260, 'Knight', 30,10, 3)
bandit1 = Charactor(400, 270, 'Bandit', 20,6, 1)
Boss1 = Charactor(700, 270, 'Bandit', 20,6, 1)

enemy_list = []
enemy_list.append(bandit1)


knight_health_bar = HealthBar(screen,100,SCREEN_HEIGHT - BOTTOM_PANEL + 40, knight.hp, knight.max_hp)
bandit_health_bar = HealthBar(screen,550,SCREEN_HEIGHT - BOTTOM_PANEL + 40, bandit1.hp, bandit1.max_hp)


#game loop
run = True
while run:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # draw panels
    draw_bg()
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit_health_bar.draw(bandit1.hp)


    # draw fighters
    knight.update()
    knight.draw(screen)
    bandit1.update()
    bandit1.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()