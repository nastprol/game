from student import Coctail


class Bar:

    def __init__(self, alcs):
        self.alcohol = alcs

    def mix(self, alc):
        coctail = Coctail()
        alc.count -= 1
        if alc.count < 0:
            raise Exception

        coctail.add_alco(alc, 1)
        return coctail

