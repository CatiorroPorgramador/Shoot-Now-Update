from cmath import rect
import pygame

class shot_class(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)

        self.image = pygame.surface.Surface([8, 3.5])
        self.image.fill((255, 235, 0))

        self.rect = pygame.Rect(0, 0, 10, 5)
        self.speed = 0
    
    def update(self, *args, **kwargs) -> None:
        if self.rect.x < -10:
            self.kill()
        elif self.rect.x > 850:
            self.kill()
        
        self.rect.x += self.speed
