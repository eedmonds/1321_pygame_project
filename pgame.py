import pygame, sys, os
import random
from Charactor import Character
from HealthBar import HealthBar

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Assets/Music/backgroundMusic.mp3')
pygame.mixer.music.play(-1) # start the music
current_enemy_index = 0  # Only this enemy will act
# Game window setup
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Adventure Arena')

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# back ground images and display panel assets
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

# Fonts
font = pygame.font.SysFont('Times New Roman', 26)

# Global list for floating damage numbers
floating_texts = []

# Turn-based state
player_turn = True
turn_transition_timer = 0

# UI button rectangles
attack_btn = pygame.Rect(100, SCREEN_HEIGHT - 85, 100, 40)
potion_btn = pygame.Rect(260, SCREEN_HEIGHT - 85, 100, 40)

# Draw functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function to for drawing background  to screen
def draw_bg():
    screen.blit(background_img, (0, 0))

# function to drawing background images to screen
def draw_panel():
    screen.blit(panel_img, (0, screen.get_height() - BOTTOM_PANEL))
    draw_text(f'{player.name} Potions: {player.potions}', font, HealthBar.red, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 10)
    player_health.draw(player.hp)
    for i, e in enumerate(enemy_list):
        draw_text(f'{e.name}', font, HealthBar.red, 550, SCREEN_HEIGHT - BOTTOM_PANEL + 10 + i * 60)
        enemy_health_bars[i].draw(e.hp)

    # Draw Buttons

    pygame.draw.rect(screen, (100, 100, 100), attack_btn)
    draw_text("Attack", font, (255, 255, 255), attack_btn.x + 10, attack_btn.y + 10)
    pygame.draw.rect(screen, (100, 100, 100), potion_btn)
    draw_text("Potion", font, (255, 255, 255), potion_btn.x + 10, potion_btn.y + 10)

def draw_turn_indicator():# Turn indicator
    if turn_transition_timer > 0:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        draw_text("Enemy Turn", font, (255, 0, 0), SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2)

def draw_floating_texts():
    for ft in floating_texts[:]:
        ft['y'] -= 1
        ft['timer'] -= 1
        draw_text(ft['text'], font, ft['color'], ft['x'], ft['y'])
        if ft['timer'] <= 0:
            floating_texts.remove(ft)

def main_menu():
    menu = True
    while menu:
        screen.fill((0, 0, 0))
        draw_text("Choose Your Hero:", font, (255, 255, 255), 300, 100)
        draw_text("1. Knight", font, (255, 255, 255), 320, 150)
        draw_text("2. Wizard", font, (255, 255, 255), 320, 200)
        draw_text("3. Thief", font, (255, 255, 255), 320, 250)
        draw_text("Q. Quit", font, (255, 255, 255), 320, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'Knight'
                elif event.key == pygame.K_2:
                    return 'Wizard'
                elif event.key == pygame.K_3:
                    return 'Thief'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


selected_class = main_menu()
player = Character(200, 260, selected_class, 60, 10, 3)

wave = 1

def create_enemies(wave):
    enemies = []
    for i in range(wave):
        enemy = Character(500 + i * 100, 260, 'Bandit', 20 + 5 * wave, 6 + wave, 1)
        enemies.append(enemy)
    return enemies

def create_enemy_health_bars():
    bars = []
    for i, e in enumerate(enemy_list):
        bar = HealthBar(screen, 550, SCREEN_HEIGHT - BOTTOM_PANEL + 40 + i * 60, e.hp, e.max_hp, animate=True)
        bars.append(bar)
    return bars

enemy_list = create_enemies(wave)
enemy_health_bars = create_enemy_health_bars()
player_health = HealthBar(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, player.hp, player.max_hp, animate=True)

def ask_to_use_potion():
    healing_popup = True
    while healing_popup:
        screen.fill((0, 0, 0))
        draw_text("You beat the enemies!", font, (255, 255, 255), 260, 150)
        draw_text("Use a potion to heal 25 HP?", font, (255, 255, 255), 240, 200)
        draw_text("Y - Yes    N - No", font, (255, 255, 255), 280, 250)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def show_wave_complete(wave_num):
    timer = 90  # Show for 1.5 seconds at 60 FPS
    while timer > 0:
        screen.fill((0, 0, 0))
        draw_text(f"Wave {wave_num} Complete!", font, (255, 255, 0), SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20)
        pygame.display.update()
        timer -= 1
        clock.tick(FPS)

def game_over_screen():
    while True:
        screen.fill((0, 0, 0))
        draw_text("You Died!", font, (255, 0, 0), SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 60)
        draw_text("Press R to Restart or Q to Quit", font, (255, 255, 255), SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main Game Loop
run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_panel()
    draw_floating_texts()

    if turn_transition_timer > 0:
        turn_transition_timer -= 1
        pygame.display.flip()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            for event in pygame.event.get():
                if event.type == pygame.quit() or event.type == pygame.KEYDOWN or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            mouse_pos = pygame.mouse.get_pos()
            if attack_btn.collidepoint(mouse_pos):
                for i, enemy in enumerate(enemy_list):
                    if enemy.alive and player.check_collision(enemy):
                        player.attack(enemy)
                        damage = player.strength + random.randint(-5, 5)
                        damage = max(0, damage)
                        enemy.hp -= damage
                        if enemy.hp <= 0:
                            enemy.hp = 0
                            enemy.alive = False
                            enemy.action = 3
                            enemy.death(enemy)
                            if i == current_enemy_index:
                                current_enemy_index += 1
                        enemy_health_bars[i].flash("damage")
                        floating_texts.append(
                            {'text': f'-{damage}', 'x': enemy.rect.x, 'y': enemy.rect.y - 20, 'color': (255, 0, 0),
                             'timer': 30})
                        player_turn = False
                        turn_transition_timer = 60
                        break

            elif potion_btn.collidepoint(mouse_pos):
                if player.potions > 0 and player.hp < player.max_hp:
                    player.hp += 20
                    if player.hp > player.max_hp:
                        player.hp = player.max_hp
                    player.potions -= 1
                    player_health.flash("heal")
                    player.idle()
                    floating_texts.append({'text': '+20', 'x': player.rect.x, 'y': player.rect.y - 20, 'color': (0, 255, 0), 'timer': 30})
                    player_turn = False
                    turn_transition_timer = 60

    player.handle_input()
    player.update()
    player.draw(screen)

    for i, enemy in enumerate(enemy_list):
        enemy.update()
        enemy.draw(screen)

    if not player_turn and turn_transition_timer == 0:
        if current_enemy_index < len(enemy_list):
            enemy = enemy_list[current_enemy_index]
            if enemy.alive:
                enemy.attack(player)
                damage = enemy.strength + random.randint(-3, 3)
                damage = max(0, damage)
                player.hp -= damage
                if player.hp <= 0:
                    player.hp = 0
                    player.alive = False
                    pygame.display.flip()
                    pygame.time.delay(500)
                    if game_over_screen():
                        selected_class = main_menu()
                        player = Character(200, 260, selected_class, 100, 10, 3)
                        player_health = HealthBar(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, player.hp,
                                                  player.max_hp, animate=True)
                        wave = 1
                        enemy_list = create_enemies(wave)
                        enemy_health_bars = create_enemy_health_bars()
                        player_turn = True
                        turn_transition_timer = 0
                        floating_texts.clear()
                        continue
                player_health.flash("damage")
                floating_texts.append(
                    {'text': f'-{damage}', 'x': player.rect.x, 'y': player.rect.y - 20, 'color': (255, 0, 0),
                     'timer': 30}
                )
            player_turn = True
            turn_transition_timer = 60
        else:
            player_turn = True
            enemy_turn_index = 0
    if all(not enemy.alive for enemy in enemy_list):
        show_wave_complete(wave)

        if player.potions > 0 and player.hp < player.max_hp:
            if ask_to_use_potion():
                player.hp += 50
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                player.potions -= 1
                player_health.flash("heal")
                floating_texts.append(
                    {'text': '+50', 'x': player.rect.x, 'y': player.rect.y - 20, 'color': (0, 255, 0), 'timer': 30})

        if wave < 2:
            wave += 1
            enemy_list = create_enemies(wave)
            enemy_health_bars = create_enemy_health_bars()
            player_turn = True

    pygame.display.flip()
#stop the music
pygame.mixer.music.stop()
pygame.quit()