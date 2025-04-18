import pygame

class HealthBar:
    red = (255, 0, 0)
    green = (0, 255, 0)
    border_color = (0, 0, 0)

    def __init__(self, surface, x, y, hp, max_hp, animate=False):
        self.surface = surface
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.current_hp = hp
        self.target_hp = hp
        self.width = 100
        self.height = 20
        self.animate = animate
        self.flash_timer = 0
        self.flash_color = None

    def flash(self, mode):
        if mode == "damage":
            self.flash_color = (255, 100, 100)
        elif mode == "heal":
            self.flash_color = (100, 255, 100)
        self.flash_timer = 10

    def draw(self, new_hp):
        if self.animate:
            self.target_hp = new_hp
            if self.current_hp < self.target_hp:
                self.current_hp += 0.5
                if self.current_hp > self.target_hp:
                    self.current_hp = self.target_hp
            elif self.current_hp > self.target_hp:
                self.current_hp -= 0.5
                if self.current_hp < self.target_hp:
                    self.current_hp = self.target_hp
        else:
            self.current_hp = new_hp

        ratio = self.current_hp / self.max_hp if self.max_hp > 0 else 0

        # Flashing effect
        if self.flash_timer > 0:
            bar_color = self.flash_color
            self.flash_timer -= 1
        else:
            bar_color = self.green

        pygame.draw.rect(self.surface, self.red, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.surface, bar_color, (self.x, self.y, self.width * ratio, self.height))
        pygame.draw.rect(self.surface, self.border_color, (self.x, self.y, self.width, self.height), 2)
