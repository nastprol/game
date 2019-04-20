from player import Player
from bar import Bar
import pygame
from student import Alcohol, Coctail
from student import Student
import random

WIDTH = 1024
HEIGHT = 768


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        self.alcs = {
            'Коньяк': Alcohol('Коньяк', 40, 2, 'img...'),
            'Водка': Alcohol('Водка', 40, 2, 'llll...'),
            'Пиво': Alcohol('Пиво', 2, 5, 'kkdfgkldf'),
            'Кола': Alcohol('Кола', 0, 9, 'dfgdfg'),
        }

        self.student_type = [
            Student(30, 0, 20, pygame.image.load('img/student3.png'), 0),
            Student(10, 5, 50, pygame.image.load('img/student1.png'), 30),
            Student(20, 20, 99, pygame.image.load('img/student2.png'), 40),
        ]

        # Картинки

        self.progressBar = []
        for i in range(15):
            self.progressBar.append(pygame.image.load(f'img/marking_{i}.png'))

        self.students = []
        for i in range(5):
            self.students.append(random.choice(self.student_type).clone(wish=random.randint(10, 40)))
        self.active_students = []

        self.back = pygame.image.load('img/back.png')
        self.cloud = pygame.image.load('img/cloud.png')
        self.cloud = pygame.transform.scale(self.cloud, (90, 90))

        self.back = pygame.transform.scale(self.back, (WIDTH, 370))
        self.bar_img = pygame.image.load('img/bar.png')
        self.bar_img = pygame.transform.scale(self.bar_img, (WIDTH, HEIGHT))

        self.alco_spot = pygame.image.load('img/alco_spot.png')
        self.alco_spot = pygame.transform.scale(self.alco_spot, (80, 150))

        self.beer = pygame.image.load('img/beer.png')
        self.beer = pygame.transform.scale(self.beer, (50, 150))
        self.vodka = pygame.image.load('img/vodka.png')
        self.vodka = pygame.transform.scale(self.vodka, (50, 150))

        self.glass = pygame.image.load('img/glass.png')
        self.glass = pygame.transform.scale(self.glass, (50, 150))

        self.bar = Bar(list(self.alcs.values()))
        self.player = Player(self.bar)

        self.spots = {(90, 525): self.alcs['Пиво'], (0, 525): self.alcs['Водка']}
        self.spot_size = (80, 150)

        self.curr_coctail = None

        self.game_over = False

        # Места для игроков
        self.free_places = {
            1: None,
            2: None,
            3: None
        }
        self.places = {
            1: (100, 100),
            2: (300, 100),
            3: (500, 100)
        }

    def menu(self):
        start_img = pygame.image.load('img/menu_start.png')
        quit_img = pygame.image.load('img/menu_quit.png')
        self.screen.blit(start_img, (300, 50))
        self.screen.blit(quit_img, (300, 100))
        pos_start = (300, 50, 620, 114)
        pos_quit = (300, 100, 620, 164)
        while True:
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN:
                    pos = i.pos

                    if (pos_start[0] <= pos[0] <= pos_start[2] and
                            pos_start[1] <= pos[1] <= pos_start[3]):
                        self.play()

                    if (pos_quit[0] <= pos[0] <= pos_quit[2] and
                            pos_quit[1] <= pos[1] <= pos_quit[3]):
                        quit()

            pygame.display.update()
        pygame.time.Clock().tick(60)

    # Общее счастье
    @property
    def happiness(self):
        h = 0
        for s in self.students:
            h += s.happiness
        return h / len(self.students)

    def finish_student(self, st):
        i = None
        if st in self.active_students:
            self.active_students.remove(st)
        st.finished = True

        self.free_places[st.position] = None
        st.position = None

    def click(self, pos):
        for s in self.spots.keys():
            if (s[0] <= pos[0] <= s[0] + self.spot_size[0]
                    and s[1] <= pos[1] <= s[1] + self.spot_size[1]):
                if self.curr_coctail is None:
                    self.curr_coctail = Coctail()
                self.curr_coctail.add_alco(self.spots[s], 0.1)
                break
        else:
            for st in self.students:
                coords = st.coord
                size = (200, 200)
                if (coords[0] <= pos[0] <= coords[0] + size[0]
                        and coords[1] <= pos[1] <= coords[1] + size[1]
                        and self.curr_coctail != None):
                    st.add_alco(self.curr_coctail)

                    self.finish_student(st)
                    self.finished.append(st)
                    self.curr_coctail = None

    def get_free_places(self):
        free = []
        for (index, st) in self.free_places.items():
            if st is None:
                free.append(index)
        return free

    def get_active_students(self):

        free = self.get_free_places()

        for student in self.students:
            if len(free) == 0:
                break
            if student not in self.finished and not student.finished:
                index = free.pop()
                self.free_places[index] = student
                student.position = index
                self.active_students.append(student)

    def draw_anecdots(self, l):
        pygame.font.init()
        myfont2 = pygame.font.SysFont('Comic Sans MS', 50)
        haha = myfont2.render('АхХАХАаХА', False, (0, 0, 0))
        l = (l + 5) % 1024
        self.screen.blit(haha, (l, 25))
        return l

    def draw_active_students(self):

        for student in self.active_students:
            student.update()

            if student.timer < 0:

                self.finish_student(student)
                self.finished.append(student)

            if student.happiness < -1:
                self.game_over = True
                return

            if student.coord < self.places[student.position]:
                student.coord = (student.coord[0] + 10, student.coord[1])

            student.img = pygame.transform.scale(student.img, (200, 300))
            self.screen.blit(student.img, student.coord)
            self.screen.blit(self.cloud, (student.coord[0] + 150, student.coord[1] - 50))

            pygame.font.init()
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            textsurface = myfont.render(str(student.wish), False, (0, 0, 0))
            self.screen.blit(textsurface, (student.coord[0] + 175, student.coord[1] - 30))

            student.draw(self.screen)

    def draw_finished_students(self):
        #print(finished)

        for student in self.finished:

            student.update()

            if student.timer < 0:
                self.finish_student(student)
                self.finished.append(student)

            if student.happiness < -1:
                self.game_over = True

            student.coord = (student.coord[0] + 30, student.coord[1])

            student.img = pygame.transform.scale(student.img, (200, 300))
            self.screen.blit(student.img, student.coord)

            student.draw(self.screen)

            if student.coord[0] >= WIDTH:
                try:
                    self.finished.remove(student)
                except:
                    pass
                try:
                    self.active_students.remove(student)
                except:
                    pass

    # Инициализация
    def play(self):

        l = 0
        self.students[0].coord = (-300, 100)
        self.finished = []

        while True:
            """
            print(len(self.students))
            for s in self.students:
                print(s.position, s.coord)
            """

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif i.type == pygame.MOUSEBUTTONDOWN:
                    pos = i.pos
                    self.click(pos)

            pygame.display.toggle_fullscreen()
            self.screen.blit(self.back, (0, 0))

            self.get_active_students()

            l = self.draw_anecdots(l)

            self.draw_active_students()
            if self.game_over:
                self.restart_menu()
            self.draw_finished_students()
            self.draw_bar()

            if self.curr_coctail:
                self.draw_coctail()

            self.max_happiness = len(self.students) * 100
            self.screen.blit(self.progressBar[int(15 * self.happiness / self.max_happiness - 0.1)], (15, 20))

            if self.game_over:
                self.restart_menu()

            pygame.display.update()

            for student in self.students:
                student.happiness -= 0.1
                student.alco_count -= 0.01

            pygame.time.Clock().tick(120)  # 60 frames per second

    def draw_bar(self):
        self.screen.blit(self.bar_img, (0, 0))
        self.screen.blit(self.alco_spot, (90, 525))
        self.screen.blit(self.alco_spot, (0, 525))
        self.screen.blit(self.beer, (105, 515))
        self.screen.blit(self.vodka, (15, 515))

    def draw_coctail(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        current = myfont.render(str(round(self.curr_coctail.level, 2)), False, (0, 0, 0))
        self.screen.blit(current, (510, 360))
        self.screen.blit(self.glass, (450, 285))

    def readkeys(self):
        pass

    def restart_menu(self):
        self.progressBar = []
        for i in range(15):
            self.progressBar.append(pygame.image.load(f'img/marking_{i}.png'))

        self.students = []
        for i in range(3):
            self.students.append(random.choice(self.student_type).clone(wish=random.randint(10, 40)))
        self.active_students = []

        self.curr_coctail = None
        self.spots = {(90, 525): self.alcs['Пиво'], (0, 525): self.alcs['Водка']}
        self.spot_size = (80, 150)

        self.game_over = False
        self.free_places = frozenset({
            1: None,
            2: None,
            3: None
        })
        self.places = {
            1: (100, 100),
            2: (300, 100),
            3: (500, 100)
        }
        self.bar = Bar(list(self.alcs.values()))
        self.player = Player(self.bar)
        self.menu()


if __name__ == "__main__":
    e = Game()
    e.menu()
