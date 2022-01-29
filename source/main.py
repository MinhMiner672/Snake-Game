from game import *

mainGame = Game()

while True:
    mainGame.events()
    mainGame.fillScreen()

    mainGame.showSnake()
    mainGame.showApple()

    mainGame.showScore()
    mainGame.getPoints()

    mainGame.update()
