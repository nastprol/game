import pygame
import random
import math
import time


class Alcohol:
    def __init__(self, name, degree, level, path):
        self.name = name
        self.degree = degree
        self.img = path
        self.count = 1000


class Coctail:
    def __init__(self):
        self.alcohols = {}
        self.mixed = False
        self.volume = 0
        self.counts = {}

    def add_alco(self, alcohol, count):
        name = alcohol.name
        if name not in self.alcohols:
            self.counts[name] = 0
            self.alcohols[name] = alcohol
        self.counts[name] += count
        self.volume += count

    def mix(self):
        self.mixed = True

    @property
    def level(self):
        lvl = 0
        for name in self.alcohols:
            lvl += self.alcohols[name].degree * self.counts[name]

        return lvl / self.volume


class Student:
    def __init__(self, happiness, alco_lvl, max_alco, img, wish):
        self.happiness = 100
        self.alco_lvl = alco_lvl
        self.max_alco = max_alco
        self.img = img
        self.wish = wish
        self.waiting = 0
        self.alco_count = 0.0
        self.inBar = False

        self.finished = False

        self.position = None

        self.coord = (0, 100)
        self.timer = 20

    def add_alco(self, coctail):
        time.sleep(0.1)
        curr_alco = self.alco_lvl + coctail.level * coctail.volume
        self.alco_count += coctail.volume
        if curr_alco > self.max_alco:
            self.happiness = -1

        self.alco_lvl = curr_alco
        coef = (self.max_alco - curr_alco) / self.max_alco

        self.happiness += coef * coctail.level * coctail.volume * (10 - abs(self.wish - coctail.level)) * 0.5

    def update(self):

        self.timer -= 60 / 1000
        self.happiness -= 0.02
        self.alco_lvl -= 0.01
        if self.alco_lvl < 0:
            self.alco_lvl = 0

    @property
    def progress_bar_happy(self):
        max_height = 80
        height = int(max_height * self.happiness / 100)
        return pygame.Rect(self.coord[0] + 180, self.coord[1] + 50 + max_height - height, 20, height)

    @property
    def progress_bar_alco(self):
        max_height = 80
        height = int(max_height * self.alco_lvl / self.max_alco)
        return pygame.Rect(self.coord[0] + 200, self.coord[1] + 50 + max_height - height, 20, height)

    def draw(self, screen):
        happy = self.progress_bar_happy
        alco = self.progress_bar_alco
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), happy)
        pygame.draw.rect(screen, pygame.Color(0, 255, 0), alco)

    def new_lap(self):
        self.wish = random.randint(0, 90)
        self.finished = False

    def clone(self, happiness=None, alco_lvl=None, max_alco=None, wish=None):
        if happiness is None:
            happiness = self.happiness
        if alco_lvl is None:
            alco_lvl = self.alco_lvl
        if max_alco is None:
            max_alco = self.max_alco
        if wish is None:
            wish = self.wish

        return Student(happiness, alco_lvl, max_alco, self.img, wish)