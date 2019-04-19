class Alcohol:
    def __init__(self, name, degree, level, path):
        self.name = name
        self.degree = degree
        self.img = path
        self.count = level


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
        return lvl


class Student:
    def __init__(self, happiness, alco_lvl, max_alco, img, wish):
        self.happiness = happiness
        self.alco_lvl = alco_lvl
        self.max_alco = max_alco
        self.img = img
        self.wish = wish
        self.waiting = 0

        self.position = None

        self.coord = (0, 100)

    def add_alco(self, coctail):
        curr_alco = self.alco_lvl + coctail.level
        if curr_alco > self.max_alco:
            self.happiness = -1

        self.alco_lvl = curr_alco
        coef = (self.max_alco - curr_alco) / self.max_alco

        self.happiness += coef * coctail.level

    def update(self):
        self.happiness -= 0.01
        self.alco_lvl -= 0.2