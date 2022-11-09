import pygame
from scripts.spritesheet import spritesheet
from random import randint

class item_class(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)

        self.items = [
            {
                'frame': 0,
                'add': [1, 0]
            },
            {
                'frame': 1,
                'add': [0, 15]
            },
            {
                'frame': 2,
                'add': [10, 0]
            },
        ]

        self.texture = spritesheet('data/items-spritesheet.png')

        self.rect = pygame.Rect(randint(0, 818), -16, 32, 32)

        self.speed:float = 5

        self.add:list = []  # 0 - coin / 0 - health
        self.stop_y = randint(0, 568)

        # Init
        self.type = self.items[randint(0, 2)]

        self.image = pygame.transform.scale(self.texture.sprite_at(pygame.Rect(16*self.type['frame'], 0, 16, 16)),
        [32, 32]).convert_alpha()
    
    def update(self, *args, **kwargs) -> None:
        if self.rect.y <= self.stop_y:
            self.rect.y += self.speed