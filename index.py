import pygame
import time

pygame.init()

pygame.display.set_mode((600, 400))

class Game:
    def __init__(self):
        self.play = True
        self.loop()

    def loop(self):
        while self.play:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    self.play = False

                


def main():
    game = Game()


if __name__ == "__main__":
    main()