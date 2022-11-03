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
                'sound': 'data/sounds/glock_shoot_sound.wav',
            },
            'parafal': {
                'frame': 1,
                'damage': 2,
                'max-ammo': 20,
                'speed': -35,
                'sleep': 10,
                'sound': 'data/sounds/glock_shoot_sound.wav',
            },
            'uzi': {
                'frame': 2,
                'damage': 0.5,
                'max-ammo': 45,
                'speed': -25,
                'sleep': 5,
                'sound': 'data/sounds/uzi_shoot_sound.wav',
            },
            'revolver': {
                'frame': 3,
                'damage': 3,
                'max-ammo': 6,
                'speed': -20,
                'sleep': 30,
                'sound': 'data/sounds/glock_shoot_sound.wav',
            }
        }

        # Sounds
        self.cur_gun = self.guns['uzi']
        self.gun_spritesheet = spritesheet('./data/guns-spritesheet.png')
        self.shoot_sound = pygame.mixer.Sound(self.cur_gun['sound'])

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
        self.can_shoot = keys[pygame.K_SPACE] and self.index_shoot > self.cur_gun['sleep']
        if self.can_shoot:
            self.index_shoot = 0
        
        self.index_shoot += 1

    def shoot(self, *shot_group: pygame.sprite.AbstractGroup):
        new_shot = shot_class(shot_group)
        new_shot.speed = self.cur_gun['speed']

        new_shot.rect.y = self.rect.y + 30
        new_shot.rect.x = self.rect.x - 30

        self.shoot_sound.play()
    
    def change_gun(self, gun:dict):
        self.cur_gun = gun

    def get_gun_sprite(self) -> pygame.Surface:
        return pygame.transform.scale(self.gun_spritesheet.sprite_at(pygame.Rect(28*self.cur_gun['frame'], 0, 28, 16)),
        [112, 64]).convert_alpha()
