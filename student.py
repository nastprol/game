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
            lvl += self.alcohols[name].degree * self.counts[name] / self.volume
        return lvl * self.volume


class Student():
    def __init__(self):
        self.happiness = 0
        self.alco_lvl = 0
        self.max_alco = 25


    def add_alco(self, coctail):
        curr_alco = self.alco_lvl + coctail.level
        if curr_alco > self.max_alco:
            self.happiness = -1

        self.alco_lvl = curr_alco
        coef = (self.max_alco - curr_alco) / self.max_alco

        self.happiness += coef * coctail.level