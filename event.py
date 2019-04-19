from player import Player
from bar import Bar
import pygame
from student import Alcohol
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
        self.active_students = []

        self.back = pygame.image.load('img/Oblivion_1920x1080.jpg')
        self.back = pygame.transform.scale(self.back, (WIDTH, HEIGHT))
        self.bar_img = pygame.image.load('img/bar.png')
        self.bar_img = pygame.transform.scale(self.bar_img, (WIDTH, HEIGHT))

        self.free_places = {
            1 : None,
            2 : None,
            3 : None
        }

        self.places = {
            1: (100, 100),
            2: (300, 100),
            3: (500, 100)
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

        self.students[0].coord = (-300, 100)

        while True:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif i.type == pygame.MOUSEBUTTONUP:
                    pos = i.pos
                    #self.player.take()

            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            self.screen.blit(self.back, (0, -HEIGHT / 2))

            for student in self.students:
                if None in self.free_places.values():

                    for (k, v) in self.free_places.items():
                        if v is None:
                            self.free_places[k] = student
                            student.position = k
                            self.active_students.append(student)
                            break

            for student in self.active_students:

                student.img = pygame.transform.scale(student.img, (200, 300))
                self.screen.blit(student.img, student.coord)

                if student.coord != self.places[student.position]:
                    student.coord = (student.coord[0] + 10, student.coord[1])

            self.screen.blit(self.bar_img, (0, 0))
            pygame.display.update()

            pygame.time.Clock().tick(120) #60 frames per second

    def readkeys(self):
        pass


if __name__ == "__main__":
    e = Game()
    e.play()
