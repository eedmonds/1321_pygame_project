import pygame



pygame.init()

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# CREATE GAME WINDOW
screen = pygame.display .set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    screen.blit(panel_img, (0,350))

#game loop
run = True
while run:



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    draw_bg()
    draw_panel()
    pygame.display.flip()

pygame.quit()