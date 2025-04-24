import os.path

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
        self.action = "Idle"  # 0: idle, 1: attack, 2: hurt, 3: death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.last_update = 0
        self.load_animations()
        self.image = self.animation_list["Idle"][self.frame_index]  # Default to idle
        self.rect = self.image.get_rect(center=(x, y))

    def load_animations(self):
        self.animation_list = {
            "Idle": [],
            "Attack": [],
            "Death": [],
            "Hurt": [],
            "Run": []
            , "Band_Death": []
        }
        for key_action, num_frames in {"Idle": 8, "Attack": 8, "Death": 8, "Hurt": 3, "Run": 8}.items():
            for i in range(0,num_frames):
                try:
                    img = pygame.image.load(os.path.join(f"img/{self.name}/{key_action}/{i}.png"))

                    img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                    self.animation_list[key_action].append(img)  # Append to the correct action list
                except FileNotFoundError:
                    print(f"Image not found: img/{self.name}/{key_action}/{i}.png")
                    break  # Stop loading if the image is not found

    def update(self):
        if self.alive:
            self.update_time = pygame.time.get_ticks()
            if self.update_time - self.last_update > 100:  # Adjust timing as needed
                self.last_update = self.update_time
                self.frame_index += 1

                # Check if the frame index exceeds the number of frames for the current action
                if self.frame_index >= len(self.animation_list[self.action]):
                    if self.action == "Attack":  # Reset to idle after attack
                        self.frame_index = 0
                        self.action = "Idle"  # Return to idle
                    else:
                        self.frame_index = 0  # Reset for other actions

                self.image = self.animation_list[self.action][self.frame_index]

    def idle(self):
        self.action = "Idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        if self.alive:
            self.action = "Attack"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def death(self, target):
        if self.alive == False:
            if self.name == "Bandit":
                self.action = "Band_Death"
            else:
                self.action = "Death"
            self.frame_index =0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx=0, dy=0):
        if self.alive:
            self.action = "Run"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.rect.x += dx

            # Clamp to screen width
            self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = 10
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(dx=-speed)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move(dx=speed)
        else:
            self.idle()



    def check_collision(self, other):
        return self.rect.colliderect(other.rect)
