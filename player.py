from student import Alcohol


class Player:

    def __init__(self, bar):
        self.speed = 10
        self.bar = bar

    def mix(self, obj):
        return self.bar.mix(obj)

    def give_coctail(self):
        pass
