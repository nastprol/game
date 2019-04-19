from player import Player
from bar import Bar
import pygame
from alcohol import Alcohol
from student import Student

WIDTH = 1024
HEIGHT = 768


class Game:
    def __init__(self):
        self.alcs = {
            'Коньяк' : Alcohol('Коньяк', 40, 2, 'img...'),
            'Водка' : Alcohol('Водка', 40, 2, 'llll...'),
            'Пиво' : Alcohol('Пиво', 2, 5, 'kkdfgkldf'),
            'Кола' : Alcohol('Кола', 0, 9, 'dfgdfg'),
        }
        self.students = [Student(0, 0, 50, pygame.image.load('img/student1.png')), Student(20, 20, 99, pygame.image.load('img/student2.png'))] #add students

        self.back = pygame.image.load('img/Oblivion_1920x1080.jpg')
        self.back = pygame.transform.scale(self.back, (WIDTH, HEIGHT))
        self.bar_img = pygame.image.load('img/bar.png')
        self.bar_img = pygame.transform.scale(self.bar_img, (WIDTH, HEIGHT))

        self.free_places = {
            1 : None,
            2 : None,
            3 : None
        }

        self.bar = Bar(list(self.alcs.values()))
        self.player = Player(self.bar_img)

    def update(self):
        for student in self.students:
            student.update()

    @property
    def happiness(self):
        h = 0
        for s in self.students:
            h += s.happiness
        return h / len(self.students)

    def play(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        pygame.display.update()
        self.screen.blit(self.back, (0, -HEIGHT / 2))
        self.screen.blit(self.bar_img, (0, 0))

        while True:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()

                elif i.type == pygame.MOUSEBUTTONUP:
                    pos = i.pos
                    #self.player.take()
                pygame.display.update()
                pygame.time.Clock().tick(60) #60 frames per second



if __name__ == "__main__":
    e = Game()
    e.play()
