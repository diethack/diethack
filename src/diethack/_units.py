def makeConverter():
    c = Converter()

    c.add('kg', 'g', 1000)
    c.add('g', 'mg', 1000)
    c.add('mg', 'mcg', 1000)
    c.add('mcg', 'ng', 1000)

    # Dietary Reference Intake Tables (USDA)
    c.add('mcg', 'IU_vitaminD', 40)

    # Dietary Reference Intake Tables (USDA)
    c.add('RAE', 'mcg_vitaminA_betacarotine', 12)

    # Dietary Reference Intake Tables (USDA)
    c.add('DFE', 'mcg_folicAcid', 0.6)

    # Dietary Supplement Fact Sheet: Vitamin A (Office of Dietary Supplements NIH)
    c.add('IU_vitaminA_betacarotine_sup', 'RAE', 0.15)

    # Dietary Supplement Fact Sheet: Vitamin E (Office of Dietary Supplements NIH)
    c.add('IU_vitaminE_d_alphatocopherol', 'mg', 0.67) # natural
    c.add('IU_vitaminE_dl_alphatocopherol', 'mg', 0.45) # synthetic

    return c

class Converter:
    def __init__(self):
        self._ratios = {}

    # unit1 == unit2 * ratio
    def add(self, unit1, unit2, ratio):
        if unit1 in self._ratios and unit2 in self._ratios[unit1]:
            return
        if unit1 not in self._ratios:
            self._ratios[unit1] = {}
        self._ratios[unit1][unit2] = float(ratio)
        self.add(unit2, unit1, 1.0 / ratio)
        for k, v in self._ratios[unit1].items():
            self.add(k, unit2, float(ratio) / v)

    def convert(self, value1, unit1, unit2):
        if unit1 == unit2 or None in (unit1, unit2):
            return value1
        elif unit1 in self._ratios and unit2 in self._ratios[unit1]:
            return value1 * self._ratios[unit1][unit2]
        else:
            raise Exception('Unsupported conversion from %s to %s' % (unit1, unit2))

    def convertDict(self, data, units):
        res = {}
        for k in list(data.keys()):
            if type(data[k]) is tuple:
                v, u = data[k]
                if type(v) is list:
                    res[k] = [self.convert(x, u, units[k]) for x in v]
                else:
                    res[k] = self.convert(v, u, units[k])
            elif type(data[k]) is dict:
                res[k] = self.convertDict(data[k], units[k])
            else:
                res[k] = data[k]
        return res
