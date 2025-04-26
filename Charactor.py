import os.path

import pygame
import random

SCREEN_WIDTH = 800  # Needed for clamping

class Character:
    def __init__(self, x, y, name, max_hp, strength, potions, alive, load_animations=True):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = alive
        self.action = "Idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.last_update = 0
        self.is_attacking = False

        if load_animations:
            self.load_animations()
            self.image = self.animation_list["Idle"][0]
        else:
            self.image = pygame.Surface((64, 64))  # temporary image for Boss
            self.animation_list = {}

        self.rect = self.image.get_rect(center=(x, y))

    def load_animations(self):
        self.animation_list = {
            "Idle": [],
            "Attack": [],
            "Death": [],
            "Hurt": [],
            "Run": []
        }
        # Load animations without excessive debug output
        for key_action, num_frames in {"Idle": 8, "Attack": 8, "Death": 8, "Hurt": 3, "Run": 8}.items():
            for i in range(num_frames):
                try:
                    img = pygame.image.load(os.path.join(f"img/{self.name}/{key_action}/{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                    self.animation_list[key_action].append(img)  # Append to the correct action list
                except FileNotFoundError:
                    print(f"Image not found: img/{self.name}/{key_action}/{i}.png")
                    break  # Stop loading if the image is not found

    def update(self):

            # Simplified animation logic
            animation_cooldown = 60  # Slower animation speed for smoother running
            self.image = self.animation_list[self.action][self.frame_index]
            
            # Update animation frame if enough time has passed
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()  # Reset timer
                self.frame_index += 1

                # Check if the frame index exceeds the number of frames for the current action
                if self.frame_index >= len(self.animation_list[self.action]):
                    if self.action == "Idle":  # Reset to idle after attack
                        self.frame_index = len(self.animation_list[self.action]) - 1
                    else:
                        self.idle()  # Return to idle


    def idle(self):
        # Store previous action before changing it
        previous_action = self.action
        self.action = "Idle"
        
        # Only reset frame index if coming from a different action
        if previous_action != "Idle":
            self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.last_update = self.update_time - 200  # Force an immediate update

    def attack(self, target):
            self.action = "Attack"
            self.frame_index = 0
            self.is_attacking = True
            self.update_time = pygame.time.get_ticks()

    def death(self, target):
            self.action = "Death"
            self.frame_index =0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx=0):
            self.action = "Run"
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.rect.x += dx

            # Clamp to screen width
            self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(dx=-speed)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move(dx=speed)
        else:
            self.idle()



    def check_collision(self, other):
        return self.rect.colliderect(other.rect)