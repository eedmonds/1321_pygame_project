import pygame, sys,os, random
from Charactor import Character
from  HealthBar import HealthBar
from Boss import Boss

pygame.init()
pygame.mixer.init()


#Load background music
pygame.mixer.music.load('Assets/Music/backgroundMusic.mp3')
pygame.mixer.music.play(-1) # start the music
death_sound = pygame.mixer.Sound('Assets/Sound/death_sound.wav')
current_enemy_index = 0  # Only this enemy will act


# Game window setup
BOTTOM_PANEL = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOTTOM_PANEL
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Adventure')

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60  # Reduce the FPS to make movements more visible

# back ground images and display panel assets
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
main_img = pygame.image.load('img/Main/MainScreen.png').convert_alpha()
boss_background_img = pygame.image.load('img/Background/boss_background.png').convert_alpha()  # Add boss background
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()

# Fonts
font = pygame.font.SysFont('Times New Roman', 26)

# Global list for floating damage numbers
floating_texts = []

# Turn-based state


# UI button rectangles
attack_btn = pygame.Rect(100, SCREEN_HEIGHT - 85, 100, 40)
potion_btn = pygame.Rect(260, SCREEN_HEIGHT - 85, 100, 40)

# Draw functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function to for drawing background  to screen
def draw_bg():
    if is_boss_level:
        screen.blit(boss_background_img, (0, 0))
    else:
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
        screen.blit(main_img, (0, 0))
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
player = Character(200, 260, selected_class, 200, 10, 3, True)

wave = 1
stagger_distance = 0
is_boss_level = False  # Track if we're on boss level
def create_enemies(wave):
    enemies = []
    for i in range(wave):
        enemy = Character(730 + i * 100 + i * stagger_distance, 260, 'Bandit', 25, 5, 1,True)
        enemies.append(enemy)
        enemy.update()

    return enemies

def create_boss():
    # Create a powerful boss with higher stats
    boss = Boss(600, 300, "Boss", 100, 12, 0, True)
    #boss.image = boss.animations["idle"][0]# ensure a starting image is set
    return [boss]  # Return as a list to be compatible with enemy_list

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

def show_boss_transition():
    timer = 180  # Show for 3 seconds at 60 FPS
    while timer > 0:
        screen.fill((0, 0, 0))
        draw_text("Prepare for Boss Battle!", font, (255, 0, 0), SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20)
        draw_text("A powerful enemy approaches...", font, (255, 200, 0), SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 20)
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
def win_screen():
    while True:
        screen.fill((0, 0, 0))
        draw_text("You Win!", font, (0, 255, 0), SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 60)
        draw_text("Press R to Restart or Q to Quit", font, (255, 255, 255), SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart game
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

    # Handle player input first
    if player.alive:
        player.handle_input()

    # Update player regardless of turn transition
    player.update()
    player.draw(screen)

    # Update and draw enemies
    enemy_speed = 2  # Slower movement for smoother animation
    for i, enemy in enumerate(enemy_list[:]):  # Use copy of list to safely remove items
        # Set stagger distance consistently
        stagger_distance = i * 50  # Give each enemy a different position

        if enemy.alive:
            # Enemy movement logic
            if enemy.rect.x > (428 + stagger_distance):  # Move towards position 428
                enemy.action = "Run"
                enemy.rect.x -= enemy_speed
            elif enemy.rect.x == (428 + stagger_distance) or enemy.rect.x < (428 + stagger_distance + enemy_speed):
                # Set enemy to idle when reaching its position
                enemy.rect.x = 428 + stagger_distance  # Ensure exact position
                enemy.idle()

            # Update and draw after all position and state changes
            enemy.update()
            enemy.draw(screen)




    # Draw turn indicator (overlay) after characters are drawn



        pygame.display.flip()
        # Don't continue - let the game process events even during transition

    # Handle enemy turn when timer reaches 0

        # Move to next enemy in the list
        if current_enemy_index < len(enemy_list):
            enemy = enemy_list[current_enemy_index]
            print(current_enemy_index)
            print(f"Enemy selected: {enemy.name}, alive: {enemy.alive}, action: {enemy.action}")
            if enemy.alive:
                # Make sure player is near enough for the enemy to attack
                if abs(enemy.rect.x - player.rect.x) < 150:  # Check if player is within attack range
                    enemy.attack(player)
                    enemy.frame_index = 0
                    enemy.update()
                    enemy.draw(screen)

                    print(f"Enemy attacking. New action: {enemy.action}")

                    # Give the animation time to play before processing damage
                      # Short delay to see the attack animation

                    damage = enemy.strength + random.randint(-5, 100)
                    damage = max(0, damage)
                    player.hp -= damage
                    if player.hp <= 0:
                        player.hp = 0
                        player.alive = False
                        player.action = "Death"

                        enemy.frame_index = 0
                        for _ in range(len(enemy.animation_list[enemy.action])):
                            player.update()  # This will already increment frame_index internally
                            player.draw(screen)
                            pygame.display.flip()
                            pygame.time.delay(200)  # Add small delay to see animation

                        death_sound.play()

                        if game_over_screen():
                            selected_class = main_menu()
                            player = Character(200, 260, selected_class, 100, 10, 3, True)
                            player_health = HealthBar(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, player.hp,
                                                  player.max_hp, animate=True)

                            enemy_list = create_enemies(wave)
                            enemy_health_bars = create_enemy_health_bars()
                            player_turn = True

                            floating_texts.clear()
                            continue
                    player_health.flash("damage")
                    floating_texts.append(
                        {'text': f'-{damage}', 'x': player.rect.x, 'y': player.rect.y - 20, 'color': (255, 0, 0),
                         'timer': 30}
                    )
                player_turn = True
                current_enemy_index += 1


        else:
            player_turn = True


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
                        # Set a flag to indicate the player is attacking
                        player.is_attacking = True
                        damage = player.strength + random.randint(-5, 5)
                        damage = max(0, damage)
                        enemy.hp -= damage
                        if enemy.hp <= 0:
                            enemy.hp = 0
                            enemy.alive = False
                            if enemy.name == "Boss":
                                enemy.play_action("Death")
                            else:
                                enemy.action = "Death"

                            enemy.frame_index = 0
                            for _ in range(len(enemy.animation_list[enemy.action])):
                                enemy.update()  # This will already increment frame_index internally
                                enemy.draw(screen)
                                pygame.display.flip()
                                pygame.time.delay(100)  # Add small delay to see animation

                            death_sound.play()
                            if i == current_enemy_index:
                                current_enemy_index += 1
                        enemy_health_bars[i].flash("damage")
                        floating_texts.append(
                            {'text': f'-{damage}', 'x': enemy.rect.x, 'y': enemy.rect.y - 20, 'color': (255, 0, 0),
                             'timer': 30})
                        player_turn = False

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

        if all(not enemy.alive for enemy in enemy_list):
            if is_boss_level:
                if win_screen():  # 🎉 Show win screen and restart if chosen
                    selected_class = main_menu()
                    player = Character(200, 260, selected_class, 100, 10, 3, True)
                    player_health = HealthBar(screen, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, player.hp, player.max_hp,
                                              animate=True)

                    wave = 1
                    is_boss_level = False
                    enemy_list = create_enemies(wave)
                    enemy_health_bars = create_enemy_health_bars()
                    floating_texts.clear()
                    current_enemy_index = 0
                    continue
            else:
                show_wave_complete(wave)
                wave += 1
                if wave == 3:
                    is_boss_level = True
                    show_boss_transition()
                    enemy_list = create_boss()
                else:
                    enemy_list = create_enemies(wave)

                enemy_health_bars = create_enemy_health_bars()
                player_turn = True
                current_enemy_index = 0


    pygame.display.flip()
#stop the music
pygame.mixer.music.stop()
pygame.quit()