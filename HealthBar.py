import pygame

class HealthBar:
    # define colors
    red = (255, 0, 0)
    green = (0, 255, 0) # change color to Blue. or purple

    def __init__(self, screen, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.screen = screen

    def draw(self, hp):
        self.hp = hp
        #calculate health ratio
        ratio = self.hp/ self.max_hp
        pygame.draw.rect(self.screen, HealthBar.red, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.screen, HealthBar.green, (self.x, self.y, 150 * ratio, 20))
