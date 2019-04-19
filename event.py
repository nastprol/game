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

        self.students = [Student(0, 0, 50, pygame.image.load('img/student1.png'), 30), Student(20, 20, 99, pygame.image.load('img/student2.png'), 40)] #add students
        self.active_students = []

        self.back = pygame.image.load('img/Oblivion_1920x1080.jpg')
        self.cloud = pygame.image.load('img/cloud.png')
        self.cloud = pygame.transform.scale(self.cloud, (90, 90))

        self.back = pygame.transform.scale(self.back, (WIDTH, HEIGHT))
        self.bar_img = pygame.image.load('img/bar.png')
        self.bar_img = pygame.transform.scale(self.bar_img, (WIDTH, HEIGHT))

        self.alco_spot = pygame.image.load('img/alco_spot.png')
        self.alco_spot = pygame.transform.scale(self.alco_spot, (80, 150))

        self.beer = pygame.image.load('img/beer.png')
        self.beer = pygame.transform.scale(self.beer, (60, 100))
        self.vodka = pygame.image.load('img/vodka.png')
        self.vodka = pygame.transform.scale(self.vodka, (60, 100))

        self.glass = pygame.image.load('img/glass.png')
        self.glass = pygame.transform.scale(self.glass, (60, 100))

        self.spots = {(90, 525) : self.alcs['Пиво'], (0, 525) : self.alcs['Водка']}
        self.spot_size = (80, 150)

        self.coctail_active = False

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
                    for s in self.spots.keys():
                        if (s[0] <= pos[0] <= s[0] + self.spot_size[0]
                                and s[1] <= pos[1] <= s[1] + self.spot_size[1]):
                            self.player.take(self.spots[s])

                            if self.spots[s].name == 'Пиво':
                                self.coctail_active = self.beer
                            else:
                                self.coctail_active = self.vodka

            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            pygame.display.toggle_fullscreen()

            self.screen.blit(self.back, (0, 0))

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
                self.screen.blit(self.cloud, (student.coord[0] + 100, student.coord[1] - 100))

                if student.coord != self.places[student.position]:
                    student.coord = (student.coord[0] + 10, student.coord[1])

            self.screen.blit(self.bar_img, (0, 0))

            self.screen.blit(self.alco_spot, (90, 525))
            self.screen.blit(self.alco_spot, (0, 525))

            self.screen.blit(self.beer, (100, 550))
            self.screen.blit(self.vodka, (10, 550))

            if self.coctail_active:
                self.screen.blit(self.coctail_active, (500, 350))

            pygame.display.update()

            pygame.time.Clock().tick(120) #60 frames per second

    def readkeys(self):
        pass


if __name__ == "__main__":
    e = Game()
    e.play()
