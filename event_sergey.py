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
        self.alcs = {
            'Коньяк': Alcohol('Коньяк', 40, 2, 'img...'),
            'Водка': Alcohol('Водка', 40, 2, 'llll...'),
            'Пиво': Alcohol('Пиво', 2, 5, 'kkdfgkldf'),
            'Кола': Alcohol('Кола', 0, 9, 'dfgdfg'),
        }
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.student_type = [
            Student(30, 0, 20, pygame.image.load('img/student3.png'), 0),
            Student(10, 5, 50, pygame.image.load('img/student1.png'), 30),
            Student(20, 20, 99, pygame.image.load('img/student2.png'), 40),
        ]

        self.progressBar = []
        for i in range(15):
            self.progressBar.append(pygame.image.load(f'img/marking_{i}.png'))

        # Картинки

        self.students = []
        for i in range(5):
            self.students.append(random.choice(self.student_type).clone(wish=random.randint(10, 40), happiness=100))
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
        self.curr_coctail = None

        self.glass = pygame.image.load('img/glass.png')
        self.glass = pygame.transform.scale(self.glass, (50, 150))

        self.spots = {(90, 525): self.alcs['Пиво'], (0, 525): self.alcs['Водка']}
        self.spot_size = (80, 150)

        self.coctail_active = False

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

        self.bar = Bar(list(self.alcs.values()))
        self.player = Player(self.bar)


    def menu(self):
        start_img = pygame.image.load('img/menu_start.png')
        quit_img = pygame.image.load('img/menu_quit.png')
        while True:
            self.screen.blit(start_img, (30, 50))
            self.screen.blit(quit_img, (30, 100))
            pos_start = (30, 50, 350, 114)
            pos_quit = (30, 100, 350, 164)
            
            for i in pygame.event.get():
                if i.type == pygame.MOUSEBUTTONDOWN:
                    pos = i.pos
                    
                    if (pos_start[0] <= pos[0] <= pos_start[2] and
                        pos_start[1] <= pos[1] <= pos_start[3]):
                        return

                    if (pos_quit[0] <= pos[0] <= pos_quit[2] and
                        pos_quit[1] <= pos[1] <= pos_quit[3]):
                        quit()

            pygame.display.update()
            
        pygame.time.Clock().tick(60)


    # всех студентов перепроверил
    def update(self):
        for student in self.students:
            student.update()

    # Общее счастье
    @property
    def happiness(self):
        h = 0
        for s in self.students:
            h += s.happiness
        return h / len(self.students)

    def finish_student(self, st):
        i = None
        for (k, v) in self.free_places.items():
            if v == st:
                i = k
                break
        st.finished = True
        self.free_places[i] = None
        self.places[i] = None
        self.coctail_active = False
        self.curr_coctail = None
        st.new_lap()
        print(self.free_places)

    def click(self, pos, finished):
        for s in self.spots.keys():
            if (s[0] <= pos[0] <= s[0] + self.spot_size[0]
                    and s[1] <= pos[1] <= s[1] + self.spot_size[1]):
                if self.curr_coctail is None:
                    self.curr_coctail = Coctail()
                self.curr_coctail.add_alco(self.spots[s], 0.1)
                self.coctail_active = True
                break
        else:
            for st in self.students:
                coords = st.coord
                size = (200, 200)
                if (coords[0] <= pos[0] <= coords[0] + size[0]
                        and coords[1] <= pos[1] <= coords[1] + size[1]
                        and self.curr_coctail != None):
                    print('student')
                    st.add_alco(self.curr_coctail)
                    self.finish_student(st)
                    finished.append(st)
                    self.curr_coctail = None

    def get_active_students(self):
        for student in self.students:
            if None in self.free_places.values():
                for (k, v) in self.free_places.items():
                    if v is None:
                        self.free_places[k] = student
                        student.position = k
                        self.active_students.append(student)
                        break

    def draw_anecdots(self, l):
        pygame.font.init()
        myfont2 = pygame.font.SysFont('Comic Sans MS', 50)
        haha = myfont2.render('АхХАХАаХА', False, (0, 0, 0))
        l = (l + 5) % 1024
        self.screen.blit(haha, (l, 25))
        return l

    def draw_active_students(self, finished):
        for student in self.active_students:
            student.update()

            print(student.timer)
            if student.timer < 0:
                self.finish_student(student)
                finished.append(student)
                print('timer', finished)

            if student.happiness < -1:
                self.game_over = True

            if student.coord != self.places[student.position]:
                student.coord = (student.coord[0] + 10, student.coord[1])

            student.img = pygame.transform.scale(student.img, (200, 300))
            self.screen.blit(student.img, student.coord)
            self.screen.blit(self.cloud, (student.coord[0] + 150, student.coord[1] - 50))

            pygame.font.init()
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            textsurface = myfont.render(str(student.wish), False, (0, 0, 0))
            self.screen.blit(textsurface, (student.coord[0] + 175, student.coord[1] - 30))

            student.draw(self.screen)

    # Инициализация
    def play(self):
        pygame.init()
        l = 0

        self.students[0].coord = (-300, 100)

        finished = []
        

        while True:

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif i.type == pygame.MOUSEBUTTONDOWN:
                    pos = i.pos
                    self.click(pos, finished)

            pygame.display.toggle_fullscreen()
            self.screen.blit(self.back, (0, 0))

            self.get_active_students()
            l = self.draw_anecdots(l)

            self.draw_active_students(finished)

            self.screen.blit(self.bar_img, (0, 0))

            self.screen.blit(self.alco_spot, (90, 525))
            self.screen.blit(self.alco_spot, (0, 525))

            self.screen.blit(self.beer, (105, 515))
            self.screen.blit(self.vodka, (15, 515))

            if self.curr_coctail:
                myfont = pygame.font.SysFont('Comic Sans MS', 30)
                current = myfont.render(str(round(self.curr_coctail.level, 2)), False, (0, 0, 0))
                self.screen.blit(current, (510, 360))

            if self.coctail_active:
                self.screen.blit(self.glass, (450, 285))

            if self.game_over:
                game_over = pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), pygame.Rect(0, 0, 1024, 768))

            self.max_happiness = len(self.students) * 100
            self.screen.blit(self.progressBar[int(15 * self.happiness / self.max_happiness - 0.1)], (15, 60))


            pygame.display.update()

            if self.game_over:
                pygame.quit()
                return

            pygame.time.Clock().tick(120)  # 60 frames per second

    def readkeys(self):
        pass


if __name__ == "__main__":
    e = Game()
    e.menu()
    e.play()
