import pygame

from random import randint
from scripts.shot import shot_class

class zombie_class(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)

        type_ids = [
            { # Simple Zombie
                'texture': './data/zombies/simple-zombie-spritesheet.png',
                'life': 1,
                'speed': 2,
                'damage': 15
            },
            { # Runner Zombie
                'texture': './data/zombies/runner-zombie-spritesheet.png',
                'life': 1,
                'speed': 4,
                'damage': 20
            },
            { # Gangster Zombie
                'texture': './data/zombies/shooter-zombie-spritesheet.png',
                'life': 2,
                'speed': 1,
                'damage': 15,
            }
        ]

        self.rect:pygame.Rect = pygame.Rect(-32, randint(0, 536), 64, 64)
        
        self.speed:int
        self.life:int
        self.damage:int
        self.id:int
        self.shot_group:pygame.sprite.AbstractGroup

        self.tmp:list = []
        self.vec = [0, 0]

        # Change Type
        self.type:dict
        type_id:int = randint(0, 10)

        if type_id >= 3:
            type_id = randint(0, 1)
            self.type = type_ids[type_id]
        elif type_id < 3:
            type_id = randint(1, 2)
            self.type = type_ids[type_id]
        
        self.image = pygame.image.load(self.type['texture'])
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.image = pygame.transform.flip(self.image, True, False)

        self.life = self.type['life']
        self.speed = self.type['speed']
        self.vec[0] = self.speed
        self.damage = self.type['damage']
        self.id = type_id

        if self.id == 2: # Zombie with gun
            self.tmp.append(0)      # Timer To Shoot
            self.tmp.append(False)  # Can Shoot

            self.shoot_sound = pygame.mixer.Sound('data/sounds/glock_shoot_sound.wav')

    def update(self, *args, **kwargs) -> None:
        self.rect.x += self.vec[0]
        if self.vec[0] != self.speed:
            self.vec[0] += 1

        if self.id == 2:
            self.tmp[0] += int(self.tmp[1])

            if self.rect.x >= 200:
                self.speed = 0
                self.vec[0] = 0
                self.tmp[1] = True
            
            if self.tmp[0] > 60:
                self.shoot()
                self.tmp[0] = 0
        
        if self.life <= 0:
            self.kill()

    def shoot(self):  # Zombie Shot Group != Player Shot Group
        new_shot = shot_class(self.shot_group)
        new_shot.speed = 20
        new_shot.rect.center = self.rect.center + pygame.math.Vector2(12, 10)

        self.shoot_sound.play()