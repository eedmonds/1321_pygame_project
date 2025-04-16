import pygame


class Charactor():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list =[]
        self.action = 1 # 0: idle, 1:attack, 2:hurt, 3: death
        self.frame_index = 0
        self.updat_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def update(self):
        animation_cooldown  = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index] # check if enough time has passed before updating
        if pygame.time.get_ticks() - self.updat_time > animation_cooldown:
            self.updat_time = pygame.time.get_ticks()

            self.frame_index += 1
            #if the amination has index out of bound set frame_index = 0.
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0


    def draw(self,function):
        function.blit(self.image, self.rect)

    def charRect(self, x ,y):
        self.rect = pygame.Rect((x,y,(80, 180)))