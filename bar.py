from student import Coctail

class Bar:

    def __init__(self, alcs):
        self.alcohol = alcs

    def mix(self, alcs):
        coctail = Coctail()
        for a in alcs:
            a.count -= 1
            if a.count < 0:
                raise Exception

            coctail.add_alco(a, 1)
        return coctail

