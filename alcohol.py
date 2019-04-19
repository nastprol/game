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

    def add_alco(self, name, count):
        if name not in self.alcohols:
            self.alcohols[name] = 0
        self.alcohols[name] += count

    def mix(self):
        self.mixed = True