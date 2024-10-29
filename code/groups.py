from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=vector(0,0)
    def update(self,dt):
        for sprite in self:
            sprite.update(dt)
    def draw(self):

        for sprite in sorted(self,key=lambda sprite:sprite.Z_index):
            self.display_surface.blit(sprite.image,sprite.rect.topleft)