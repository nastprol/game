

class Bar:

    def __init__(self, alcs):
        self.alcohol = alcs

    def mix(self, alcs):
        coctail = {}
        for a in alcs:
            a.count -= 1
            if a.count < 0:
                raise Exception

            coctail[a.name] += 1
        return coctail

