from player import Player
from bar import Bar
import pygame


class Event:
    def __init__(self):
        self.students = [] #add students
        alcs = []
        self.bar = Bar(alcs)
        self.player = Player(self.bar)

    def play(self):
        pygame.init()
        pygame.display.set_mode((600,400), pygame.RESIZABLE)

        pygame.display.update()

        while True:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()

                elif i.type == pygame.MOUSEBUTTONUP:
                    pos = i.pos
                    self.player.take()




if __name__ == "__main__":
    e = Event()