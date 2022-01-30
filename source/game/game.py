import pygame
from sys import exit
from .constants import *
from .sprites import *
from random import randint


pygame.init()


def show_info(info: str, y_pos=10, x_pos=10, font_size=30) -> None:
    """
    Shows a piece of information onto the display surface
    This helps you to track the change of variables
    """

    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("Arial", font_size)
    font.bold = True
    info_text_surf = font.render(str(info), True, (255, 255, 255))
    info_text_rect = info_text_surf.get_rect(center=(x_pos, y_pos))
    screen.blit(info_text_surf, info_text_rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Snake Game")

        self.score = 0

        self.snakeGroup = pygame.sprite.GroupSingle(Snake())
        self.appleGroup = pygame.sprite.GroupSingle()

        self.pressTicks = pygame.time.get_ticks()

        self.gameOver = False
        self.deathSoundPlayed = False

    def fillScreen(self):
        self.screen.fill((0, 0, 0))

    def showSnake(self):
        """Shows the snake and its body"""

        if not self.gameOver:
            self.snakeGroup.sprite.teleportation()
            self.snakeGroup.sprite.body.update()
            self.snakeGroup.update()
        else:
            if not self.deathSoundPlayed:
                deathSound = pygame.mixer.Sound("./game/sound/death.mp3")
                deathSound.play()
                self.deathSoundPlayed = True

            show_info("YOU LOST HAHA =)))", x_pos=WIDTH / 2, y_pos=100, font_size=50)

            self.appleGroup.empty()
            self.snakeGroup.sprite.loseAnimation()

        self.snakeGroup.draw(self.screen)
        self.snakeGroup.sprite.body.draw(self.screen)
        self.gameOver = self.snakeGroup.sprite.snakeCollision(self.gameOver)

    def showApple(self):
        """Shows an apple in a random position"""

        if not self.appleGroup.sprites() and not self.gameOver:
            self.appleGroup.add(Apple(randint(0, 19), randint(0, 19)))

            # Check if the position of the apple is occupied by the snake
            for body in self.snakeGroup.sprite.body.sprites():
                applePosition = (
                    self.appleGroup.sprite.x_index,
                    self.appleGroup.sprite.y_index,
                )
                snake_x_pos, snake_y_pos = (
                    self.snakeGroup.sprite.x_index,
                    self.snakeGroup.sprite.y_index,
                )

                # If the snake's position or one of the snake bodies's position is the same as apple's position
                # as soon as the apple gets spawned
                if (snake_x_pos, snake_y_pos) == applePosition or (
                    body.x_index,
                    body.y_index,
                ) == applePosition:
                    # Remove the apple
                    self.appleGroup.sprite.kill()

                    # Respawn the apple at a new position, and repeat the loop
                    self.appleGroup.add(Apple(randint(0, 19), randint(0, 19)))
                    continue

        self.appleGroup.draw(self.screen)

    def showScore(self):
        """Shows the current score of the game"""

        show_info(str(self.score), x_pos=16, y_pos=20, font_size=25)

    def getPoints(self):
        """If the snake eats an apple"""

        if not self.gameOver and self.snakeGroup.sprite.rect.colliderect(
            self.appleGroup.sprite.rect
        ):
            eatingSound = pygame.mixer.Sound("./game/sound/eating.mp3")
            eatingSound.play()

            self.score += 1
            self.appleGroup.sprite.kill()

            # Add one body cell to the snake
            self.snakeGroup.sprite.addBody()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.gameOver:
                    self.gameOver, self.deathSoundPlayed = False, False
                    self.score = 0

                # If the key is an arrow key
                if event.key in [
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_RIGHT,
                    pygame.K_LEFT,
                ]:
                    # If the interval between the last mouse click and now is 0.1s (100 milliseconds)
                    # this prevents the snake from too early direction change
                    if not pygame.time.get_ticks() - self.pressTicks >= 50:
                        return
                    else:
                        self.pressTicks = pygame.time.get_ticks()

                if event.key == pygame.K_LEFT:
                    # The arrow key pressed must not be the same as or opposite to the snake's current direction
                    if self.snakeGroup.sprite.direction in ["left", "right"]:
                        return

                    # Add where the snake changes direction and the direction to every
                    # body cell
                    for body_cell in self.snakeGroup.sprite.body.sprites():
                        body_cell.turns.append(
                            [
                                (
                                    self.snakeGroup.sprite.x_index,
                                    self.snakeGroup.sprite.y_index,
                                ),
                                "left",
                            ]
                        )

                    # Then change the direction of the snake if everything is fine
                    self.snakeGroup.sprite.direction = "left"

                if event.key == pygame.K_RIGHT:
                    if self.snakeGroup.sprite.direction in ["left", "right"]:
                        return

                    for body_cell in self.snakeGroup.sprite.body.sprites():
                        body_cell.turns.append(
                            [
                                (
                                    self.snakeGroup.sprite.x_index,
                                    self.snakeGroup.sprite.y_index,
                                ),
                                "right",
                            ]
                        )

                    self.snakeGroup.sprite.direction = "right"

                if event.key == pygame.K_UP:
                    if self.snakeGroup.sprite.direction in ["up", "down"]:
                        return

                    for body_cell in self.snakeGroup.sprite.body.sprites():
                        body_cell.turns.append(
                            [
                                (
                                    self.snakeGroup.sprite.x_index,
                                    self.snakeGroup.sprite.y_index,
                                ),
                                "up",
                            ]
                        )

                    self.snakeGroup.sprite.direction = "up"

                if event.key == pygame.K_DOWN:
                    if self.snakeGroup.sprite.direction in ["up", "down"]:
                        return

                    for body_cell in self.snakeGroup.sprite.body.sprites():
                        turn = [
                            (
                                self.snakeGroup.sprite.x_index,
                                self.snakeGroup.sprite.y_index,
                            ),
                            "down",
                        ]
                        body_cell.turns.append(turn)
                        # break

                    self.snakeGroup.sprite.direction = "down"

    def update(self):
        pygame.display.update()
        self.clock.tick(FPS)
