import pygame
import random
from Charactor import Character

class Boss(Character):
    def __init__(self, x, y, name, max_hp, strength, potions, alive):
        # Prevent Character from loading default animations
        super().__init__(x, y, name, max_hp, strength, potions, alive, load_animations=False)

        # Load sprite sheet animations (each row is a separate file)
        self.animations = {
            "idle": self.load_sprite_sheet("img/Boss/Idle/idle.png", 64, 64),
            "run": self.load_sprite_sheet("img/Boss/Run/run.png", 64, 64),
            "attack": self.load_sprite_sheet("img/Boss/Attack/attack.png", 64, 64),
            "death": self.load_sprite_sheet("img/Boss/Death/death.png", 64, 64)
        }

        # Animation setup
        self.current_action = "idle"
        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_speed = 0.12  # seconds per frame
        self.loop_animation = True

        # Set first frame and rect
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(center=(x, y))

        # Boss-specific logic
        self.special_attack_cooldown = 0
        self.special_attack_damage = int(self.strength * 1.5)
        self.phase = 1
        self.phase_thresholds = {2: 0.5}  # Go to phase 2 when below 50% HP

    def load_sprite_sheet(self, filepath, frame_width, frame_height):
        sheet = pygame.image.load(filepath).convert_alpha()
        sheet_width = sheet.get_width()
        num_frames = sheet_width // frame_width
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * 3, frame_height * 3))  # Optional scaling
            frames.append(frame)
        return frames

    def play_action(self, action, loop=True):
        if action != self.current_action:
            self.current_action = action
            self.frame_index = 0
            self.loop_animation = loop
            self.last_update_time = pygame.time.get_ticks()

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.animation_speed * 1000:
            self.last_update_time = now
            frames = self.animations[self.current_action]
            if self.loop_animation:
                self.frame_index = (self.frame_index + 1) % len(frames)
            else:
                if self.frame_index < len(frames) - 1:
                    self.frame_index += 1

    def update(self):
        # Only handle animation and boss-specific logic
        self.update_animation()

        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1

        # Phase change logic
        health_percent = self.hp / self.max_hp
        for phase, threshold in self.phase_thresholds.items():
            if health_percent <= threshold and self.phase < phase:
                self.phase = phase
                self.strength += 2
                self.special_attack_damage = int(self.strength * 1.5)

    def draw(self, surface):
        frame = self.animations[self.current_action][self.frame_index]
        surface.blit(frame, self.rect.topleft)

    # Override animation-based actions
    def idle(self):
        self.play_action("idle")

    def attack(self, target):
        self.play_action("attack", loop=False)

    def death(self, target=None):
        self.play_action("death", loop=False)

    def special_attack(self, target):
        if self.special_attack_cooldown <= 0:
            self.attack(target)  # Play attack animation
            damage = self.special_attack_damage + random.randint(0, 10)
            self.special_attack_cooldown = 3
            return damage
        return 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.death()
        return amount

    def choose_action(self, player):
        if self.special_attack_cooldown <= 0 and random.random() < 0.4:
            return "special_attack"
        else:
            return "attack"
