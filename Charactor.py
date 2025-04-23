import pygame
import random

SCREEN_WIDTH = 800  # Needed for clamping

class Character:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = True
        self.action = 0  # 0: idle, 1: attack, 2: hurt, 3: death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.load_animations()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def load_animations(self):
        self.animation_list = []
        for action in ['Idle', 'Attack','Death','Hurt','Run']:
            temp_list = []
            for i in range(8):
                try:
                    img = pygame.image.load(f'img/{self.name}/{action}/{i}.png')
                    img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                    temp_list.append(img)
                except:
                    break
            self.animation_list.append(temp_list)

    def update(self):
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        if self.alive:
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def death(self, target):
        if self.alive == False:
            self.action = 2
            self.frame_index =0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx=0, dy=0):
        if self.alive:
            self.action = 4
            self.rect.x += dx

            # Clamp to screen width
            self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = 10
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(dx=-speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move(dx=speed)
        if keys[pygame.K_UP]:
            self.move(dy=-speed)
        if keys[pygame.K_DOWN]:
            self.move(dy=speed)

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)
