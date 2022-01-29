import pygame


class Apple(pygame.sprite.Sprite):
    def __init__(self, x_index: int, y_index: int):
        super().__init__()

        self.x_index = x_index
        self.y_index = y_index

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(30 * x_index, 30 * y_index))
