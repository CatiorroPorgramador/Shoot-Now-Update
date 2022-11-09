import pygame

class spritesheet:
    def __init__(self, filename:str) -> None:
        try:
            self.texture = pygame.image.load(filename)
        except pygame.error as e:
            print('Unable to load spritesheet texture for spritesheet')
            raise SystemExit(e)
        
        self.frame = 0
    
    def sprite_at(self, rectangle:pygame.Rect) -> pygame.Surface:
        sprite:pygame.Surface = pygame.Surface(rectangle.size)
        sprite.blit(self.texture, (0, 0), rectangle)
        sprite.set_colorkey((215, 0, 255, 255))

        return sprite