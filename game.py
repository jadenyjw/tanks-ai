import pygame

class Tank(pygame.sprite.DirtySprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load(image)
        self.file = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.bullets = []
        self.rect.x = x - 32
        self.rect.y = y - 32

        loc = self.image.get_rect().center
        self.image = pygame.transform.rotate(self.image, -angle - 90)
        self.image.get_rect().center = loc
        self.current_angle = angle

    def set_position(self, x, y):
        self.rect.x = x - 32
        self.rect.y = y - 32

    def rot_center(self, angle):

        orig_rect = self.file.get_rect()
        self.image = pygame.transform.rotate(self.file, -angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = self.image.get_rect().center
        self.image = self.image.subsurface(rot_rect).copy()


    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_position(self, x, y):
        self.rect.x = x - 5
        self.rect.y = y - 5


    def draw(self, surface):
        surface.blit(self.image, self.rect)
