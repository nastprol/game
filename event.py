from player import Player
from bar import Bar
import pygame
from alcohol import Alcohol


class Event:
    def __init__(self):
        self.alcs = {
            'Коньяк' : Alcohol('Коньяк', 40, 2, 'img...'),
            'Водка' : Alcohol('Водка', 40, 2, 'llll...'),
            'Пиво' : Alcohol('Пиво', 2, 5, 'kkdfgkldf'),
            'Кола' : Alcohol('Кола', 0, 9, 'dfgdfg'),
        }
        self.students = [Student(0, 0, 50), Student(20, 20, 99)] #add students

        self.free_places = {
            1 : None,
            2 : None,
            3 : None
        }

        self.bar = Bar(list(alcs.values()))
        self.player = Player(self.bar)

    @property
    def happiness(self):
        h = 0
        for s in self.students:
            h += s.happiness
        return h / len(self.students)

    def play(self):
        pygame.init()
        pygame.display.set_mode((600, 400), pygame.RESIZABLE)

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