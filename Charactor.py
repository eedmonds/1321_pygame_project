import os.path

import pygame
import random

SCREEN_WIDTH = 800  # Needed for clamping

class Character:
    def __init__(self, x, y, name, max_hp, strength, potions, alive):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions = potions
        self.alive = alive
        self.action = "Idle"  # 0: idle, 1: attack, 2: hurt, 3: death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.last_update = 0
        self.is_attacking = False
        self.load_animations()
        self.image = self.animation_list["Idle"][0]  # Initialize image with first frame
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


class Boss(Character):
    def __init__(self, x, y, name, max_hp, strength, potions, alive):
        super().__init__(x, y, name, max_hp, strength, potions, alive)
        self.special_attack_cooldown = 0
        self.special_attack_damage = int(self.strength * 1.5)
        self.shield_active = False
        self.shield_duration = 0
        self.phase = 1  # Boss phases for different attack patterns
        self.phase_thresholds = {2: 0.5}  # Phase 2 starts at 50% health

    def update(self):
        super().update()
        
        # Manage cooldowns
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
            
        # Manage shield
        if self.shield_active:
            self.shield_duration -= 1
            if self.shield_duration <= 0:
                self.shield_active = False
                
        # Check for phase transitions
        current_health_percentage = self.hp / self.max_hp
        for phase, threshold in self.phase_thresholds.items():
            if current_health_percentage <= threshold and self.phase < phase:
                self.phase = phase
                self.strength += 2  # Increase strength in later phases
                
    def special_attack(self, target):
        if self.special_attack_cooldown <= 0:
            self.action = "Attack"
            self.frame_index = 0
            self.is_attacking = True
            self.update_time = pygame.time.get_ticks()
            
            # Special attack does more damage than regular attack
            damage = self.special_attack_damage + random.randint(0, 10)
            
            # Reset cooldown (3 turns)
            self.special_attack_cooldown = 3
            
            return damage
        return 0
        
    def activate_shield(self):
        if not self.shield_active:
            self.shield_active = True
            self.shield_duration = 2  # Lasts for 2 turns
            
    def take_damage(self, amount):
        # If shield is active, reduce damage by 50%
        if self.shield_active:
            amount = int(amount * 0.5)
            
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.action = "Death"
            
        return amount  # Return actual damage dealt

    def choose_action(self, player):
        # AI decision making for boss
        if self.hp < self.max_hp * 0.3 and not self.shield_active and random.random() < 0.7:
            # When low on health, likely activate shield
            self.activate_shield()
            return "shield"
        elif self.special_attack_cooldown <= 0 and random.random() < 0.4:
            # 40% chance to use special attack if available
            return "special_attack"
        else:
            # Regular attack
            return "attack"
