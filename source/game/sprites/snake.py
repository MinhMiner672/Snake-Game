import pygame
from ..constants import *
from random import choice


class Snake(pygame.sprite.Sprite):
    def __init__(self, direction: str = choice(["up", "down", "right", "left"])):
        super().__init__()

        self.direction = direction

        # This image's direction is already 'up' so there's no need to check if self.direction == 'up'
        # self.image = pygame.image.load('./images/snake_head.png').convert()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))

        self.x_index, self.y_index = 10, 10

        self.startMoveTicks = pygame.time.get_ticks()

        self.rect = self.image.get_rect(topleft=(self.x_index * 30, self.x_index * 30))

        self.body = pygame.sprite.Group().copy()
        self.speedVelocity = 0

        self.startLoseTicks = pygame.time.get_ticks()

    def move(self):
        """Moves the snake based on self.direction"""

        # If the velocity is more than 1.5, then reset the velocity
        if self.speedVelocity >= 1.5:
            self.speedVelocity = 0

        # We will increase the x and y index using the integer of the velocity
        # based on the snake direction
        if self.direction == "up":
            self.y_index -= int(self.speedVelocity)
        if self.direction == "down":
            self.y_index += int(self.speedVelocity)
        if self.direction == "left":
            self.x_index -= int(self.speedVelocity)
        if self.direction == "right":
            self.x_index += int(self.speedVelocity)

        # Increase the velocity until it reaches
        self.speedVelocity += 0.3

        # Update the position of the snake rectangle since the x and y index are updated constantly
        self.rect.x = 30 * self.x_index
        self.rect.y = 30 * self.y_index

    def teleportation(self):
        """If the snake goes beyond the screen, then teleport it to the opposite side"""

        if self.x_index >= 20:
            self.x_index = 0
        if self.x_index <= -1:
            self.x_index = 19
        if self.y_index >= 20:
            self.y_index = 0
        if self.y_index <= -1:
            self.y_index = 19

    def addBody(self):
        # If the snake has no body cells
        if not self.body.sprites():
            if self.direction == "up":
                newBody = SnakeBody(
                    self.x_index,
                    self.y_index + 1,
                    self.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)

            if self.direction == "down":
                newBody = SnakeBody(
                    self.x_index,
                    self.y_index - 1,
                    self.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)

            if self.direction == "left":
                newBody = SnakeBody(
                    self.x_index + 1,
                    self.y_index,
                    self.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)

            if self.direction == "right":
                newBody = SnakeBody(
                    self.x_index - 1,
                    self.y_index,
                    self.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)

        else:
            # Add the body cell based on the position of the last body cell of the snake
            lastBodyCell = self.body.sprites()[-1]
            newBody = None
            if lastBodyCell.direction == "up":
                newBody = SnakeBody(
                    lastBodyCell.x_index,
                    lastBodyCell.y_index + 1,
                    lastBodyCell.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)
            if lastBodyCell.direction == "down":
                newBody = SnakeBody(
                    lastBodyCell.x_index,
                    lastBodyCell.y_index - 1,
                    lastBodyCell.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)
            if lastBodyCell.direction == "right":
                newBody = SnakeBody(
                    lastBodyCell.x_index - 1,
                    lastBodyCell.y_index,
                    lastBodyCell.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)
            if lastBodyCell.direction == "left":
                newBody = SnakeBody(
                    lastBodyCell.x_index + 1,
                    lastBodyCell.y_index,
                    lastBodyCell.direction,
                    self.speedVelocity,
                )
                self.body.add(newBody)

            # When a new body cell is added, make its 'turns' property the same as the second last body cell
            self.body.sprites()[-1].turns = self.body.sprites()[-2].turns.copy()

    def loseAnimation(self):
        """
        If user loses the game, then the snake will die gradually, like an animation

        Args:
            gameCondition (bool): the game state
        """

        if pygame.time.get_ticks() - self.startLoseTicks >= 100:
            if self.body.sprites():
                self.body.sprites()[-1].kill()
                self.startLoseTicks = pygame.time.get_ticks()

    def snakeCollision(self, gameOver) -> bool:
        """
        This function will have an influence on the game state based
        on whether user loses the game or not

        Returns:
            bool: The final game state
        """

        if gameOver:
            return True

        # If the snake head touches on of its body cells
        for body in self.body.sprites():
            if self.rect.colliderect(body.rect):
                return True

        return False

    def update(self):
        self.move()


class SnakeBody(pygame.sprite.Sprite):
    def __init__(
        self, x_index: int, y_index: int, body_direction: str, snake_speed_velocity: int
    ):
        super().__init__()

        self.turns = []
        self.x_index = x_index
        self.y_index = y_index

        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(30 * x_index, 30 * y_index))

        self.direction = body_direction
        self.speedVelocity = snake_speed_velocity

    def moveBody(self):
        # Teleport the body cell
        if self.x_index >= 20:
            self.x_index = 0
        if self.x_index <= -1:
            self.x_index = 19
        if self.y_index >= 20:
            self.y_index = 0
        if self.y_index <= -1:
            self.y_index = 19

        if self.speedVelocity >= 1.5:
            self.speedVelocity = 0

        if self.direction == "up":
            self.y_index -= int(self.speedVelocity)
        if self.direction == "down":
            self.y_index += int(self.speedVelocity)
        if self.direction == "left":
            self.x_index -= int(self.speedVelocity)
        if self.direction == "right":
            self.x_index += int(self.speedVelocity)

        self.speedVelocity += 0.3

        self.rect = self.image.get_rect(topleft=(30 * self.x_index, 30 * self.y_index))

    def followSnake(self):
        # If the snake is still moving and not turning
        if not self.turns:
            return

        # If the snake turns and its position has been recorded
        # Example of self.turns: [(x, y), 'up']
        if (self.x_index, self.y_index) == self.turns[0][0]:
            self.direction = self.turns[0][1]
            self.turns.pop(0)

    def update(self):
        self.moveBody()
        self.followSnake()
