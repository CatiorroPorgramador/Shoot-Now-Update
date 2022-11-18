import pygame

from scripts.shot import shot_class
from scripts.spritesheet import spritesheet

class player_class(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)

        self.image = pygame.image.load('./data/player/player-spritesheet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [64, 64])
        
        self.rect:pygame.Rect = pygame.Rect(600, 268, 64, 64)
        self.speed:int = 4
        self.life:int = 100
        self.kills:int = 0 ; self.coins:int = 0
        self.shoot_sound:pygame.mixer.Sound = None

        self.guns = {
            'glock': {
                'frame': 0,
                'damage': 1,
                'max-ammo': 12,
                'speed': -25,
                'sleep': 20,
                'sound': 0,
                'position': [0, 30]
            },
            'parafal': {
                'frame': 1,
                'damage': 3,
                'max-ammo': 20,
                'speed': -35,
                'sleep': 10,
                'sound': 'data/sounds/glock_shoot_sound.wav',
                'position': [52, 28]
            },
            'uzi': {
                'frame': 2,
                'damage': 0.5,
                'max-ammo': 45,
                'speed': -25,
                'sleep': 5,
                'sound': 1,
                'position': [2, 28]
            },
            'revolver': {
                'frame': 3,
                'damage': 3,
                'max-ammo': 6,
                'speed': -20,
                'sleep': 30,
                'sound': 2,
                'position': [0, 30]
            },
            'm16': {
                'frame': 4,
                'damage': 2,
                'max-ammo': 30,
                'speed': -30,
                'sleep': 6,
                'sound': 3,
                'position': [52, 28]
            }
        }

        self.id_gun:int = 0
        self.pgun = [
            self.guns['m16'],
            self.guns['glock']
        ]

        # Sounds
        self.sounds = [
            pygame.mixer.Sound('data/sounds/glock_shoot_sound.wav'),
            pygame.mixer.Sound('data/sounds/uzi_shoot_sound.wav'),
            pygame.mixer.Sound('data/sounds/revolver_shoot_sound.wav'),
            pygame.mixer.Sound('data/sounds/m16_shoot_sound.wav')
        ]

        for sound in self.sounds:
            sound.set_volume(0.2)

        self.gun_spritesheet = spritesheet('./data/guns-spritesheet.png')
        self.shoot_sound = self.sounds[self.pgun[self.id_gun]['sound']]

        self.can_shoot:bool = False
        self.can_kick:bool = False
        self.index_shoot:int = 0

        # Init

    def update(self, *args, **kwargs) -> None:
        keys = pygame.key.get_pressed()
        
        # Movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 786:
            self.rect.x = 786
        
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y > 536:
            self.rect.y = 536
        
        # Gun Stuff
        self.can_shoot = keys[pygame.K_SPACE] and self.index_shoot > self.pgun[self.id_gun]['sleep']
        if self.can_shoot:
            self.index_shoot = 0
        
        self.index_shoot += 1

    def set_id_gun(self, id:int):
        if id < len(self.pgun):
            self.id_gun = id

    def update_gun(self) -> None:
        self.shoot_sound = self.sounds[self.pgun[self.id_gun]['sound']]

    def shoot(self, *shot_group: pygame.sprite.AbstractGroup):
        new_shot = shot_class(shot_group)
        new_shot.speed = self.pgun[self.id_gun]['speed']

        new_shot.rect.x = self.rect.x - self.pgun[self.id_gun]['position'][0]
        new_shot.rect.y = self.rect.y + self.pgun[self.id_gun]['position'][1]

        self.shoot_sound.play()

    def get_gun_sprite(self) -> pygame.Surface:
        return pygame.transform.scale(self.gun_spritesheet.sprite_at(pygame.Rect(28*self.pgun[self.id_gun]['frame'], 0, 28, 16)),
        [112, 64]).convert_alpha()
