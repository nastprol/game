class Player:

    def __init__(self, bar):
        self.speed = 10
        self.direction = 0
        self.objects = []
        self.bar = bar

    def take(self, obj):
        self.objects.append(obj)

    def mix(self):
        alcohol = []
        for o in self.objects:
            if o is Alcohol:
                alcohol.append(o)

        return self.bar.mix(alcohol)

    def give_coctail(self):
        return self.mix()
