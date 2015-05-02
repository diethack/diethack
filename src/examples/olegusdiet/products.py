from diethack import makeProduct, makeProductUnits, makeElements, \
                     fetchUsda, fetchUsdaCodes, makeConverter
from random import shuffle

def products():
    return _chickenBreast() + \
           _soyProteinSprouts() + \
           _soybeanOil() + \
           _codLiverOil() + \
           _barley() + \
           _brownRiceShort() + \
           _whiteRiceLong() + \
           _wheatBran() + \
           _sugar() + \
           _tableSalt() + \
           _distilledWater() + \
           _microSupplements()

def _microSupplements():
    return _tableSalt() + \
           _optiMen() + \
           _cholineTablets() + \
           _chromiumTablets() + \
           _iodineTablets() + \
           _biotinTablets() + \
           _molybdenumTablets() + \
           _potassiumPowder() + \
           _potassiumTablets() + \
           _floricalTablets() + \
           _calciumTablets() + \
           _magnesiumTablets() + \
           _ironTablets() + \
           _vitaminCTablets() + \
           _vitaminKTablets() + \
           _zincTablets() + \
           _riboflavinTablets() + \
           _vitaminB12Tablets() + \
           _vitaminB6Tablets() + \
           _copperTablets() + \
           _vitaminETablets() + \
           _seleniumTablets() + \
           _vitaminDTablets()

def _convert(**kwargs):
    return makeConverter().convertDict(kwargs, makeProductUnits())

def _soyProteinSprouts():
    return [makeProduct(**dict(
        fetchUsda('16122').items() + {
        'name': 'soy protein isolate bulk "sprouts"',
        'nameShort': 'soy protein',
        'price': 699,
        'priceMass': 453}.items()))]

def _chickenBreast():
    return [makeProduct(**dict(
        fetchUsda('05062').items() + {
        'name': 'boneless skinless chicken breasts "sprouts"',
        'nameShort': 'chicken breasts',
        'price': 199, # weekly special
        'priceMass': 453}.items()))]

def _soybeanOil():
    oilDensK = 0.922
    return [makeProduct(**dict(
        fetchUsda('04044').items() + {
        'name': 'soybean oil "carlini" (aldi)',
        'nameShort': 'soybean oil',
        'price': 629,
        'priceMass': 8.0*453.0*oilDensK}.items()))]

def _codLiverOil():
    return [makeProduct(**dict(
        fetchUsda('04589').items() + {
        'name': 'cod liver oil "twinlab"',
        'nameShort': 'cod liver oil',
        'dataUrl': 'http://www.vitacost.com/twinlab-norwegian-cod-liver-oil-unflavored-12-fl-oz',
        'price': 897,
        'priceMass': 355}.items()))]

def _brownRiceShort():
    return [makeProduct(**dict(
        fetchUsda('20040').items() + {
        'name': 'brown rice short-grain bulk "sprouts"',
        'nameShort': 'brown rice',
        'price': 99,
        'priceMass': 453}.items()))]

def _whiteRiceLong():
    return [makeProduct(**dict(
        fetchUsda('20044').items() + {
        'name': 'white rice long-grain bulk "sprouts"',
        'nameShort': 'white rice',
        'price': 99,
        'priceMass': 453}.items()))]

def _barley():
    return [makeProduct(**dict(
        fetchUsda('20005').items() + {
        'name': 'pearl barley bulk "sprouts"',
        'nameShort': 'barley',
        'price': 99,
        'priceMass': 453}.items()))]

def _sugar():
    return [makeProduct(**dict(
        fetchUsda('19336').items() + {
        'name': 'granulated sugar "baker\'s corner" (aldi)',
        'nameShort': 'sugar',
        'price': 149,
        'priceMass': 4*453}.items()))]

def _wheatBran():
    return [makeProduct(**dict(
        fetchUsda('20077').items() + {
        'name': 'wheat bran "bob\'s red mill"',
        'nameShort': 'wheat bran',
        'dataUrl': 'http://www.amazon.com/gp/product/B004VLVIL4',
        'price': 965,
        'priceMass': 2268}.items()))]

def _tableSalt():
    return [makeProduct(**dict(
        fetchUsda('02047').items() + {
        'name': 'table salt "morton"',
        'nameShort': 'salt',
        'price': 97,
        'priceMass': 1800}.items()))]

def _optiMen():
    # source: package
    return [makeProduct(
        name = 'vitamins opti-men "optimum nutrition"',
        price = 2149,
        priceMass = 180,
        **_convert(
            elementsMass = (3, 'g'), # 3 tablets
            elements = makeElements(
                calcium = (200, 'mg'),
                vitaminA = (10000, 'IU_vitaminA_betacarotine_sup'),
                vitaminC = (300, 'mg'),
                vitaminD = (300, 'IU_vitaminD'),
                vitaminE = (200, 'IU_vitaminE_d_alphatocopherol'),
                vitaminESup = (200, 'IU_vitaminE_d_alphatocopherol'),
                vitaminK = (75, 'mcg'),
                thiamin = (75, 'mg'),
                riboflavin = (75, 'mg'),
                niacin = (75, 'mg'),
                niacinSup = (75, 'mg'),
                vitaminB6 = (50, 'mg'),
                folate = (600, 'mcg_folicAcid'),
                folateSup = (600, 'mcg_folicAcid'),
                vitaminB12 = (100, 'mcg'),
                pantothenicAcid = (75, 'mg'),
                biotin = (300, 'mcg'),
                choline = (10, 'mg'),
                chromium = (120, 'mcg'),
                copper = (2, 'mg'),
                iodine = (150, 'mcg'),
                magnesium = (100, 'mg'),
                magnesiumSup = (100, 'mg'),
                manganese = (5, 'mg'),
                molybdenum = (80, 'mcg'),
                selenium = (200, 'mcg'),
                zinc = (30, 'mg'),
                boron = (2, 'mg'),
                silicon = (5, 'mg'),
                vanadium = (100, 'mcg')
        )))]

def _distilledWater():
    return [makeProduct(
        name = 'distilled water',
        nameShort = 'water',
        price = 0,
        priceMass = 100,
        **_convert(
            elementsMass = (100, 'g'),
            elements = makeElements(
                water = (100, 'g')
        )))]

def _cholineTablets():
    # source: online shop
    return [makeProduct(
        name = 'choline tablets "nature\'s way"',
        nameShort = 'choline',
        dataUrl = 'http://www.vitacost.com/natures-way-choline',
        price = 639,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                choline = (500, 'mg')
        )))]

def _chromiumTablets():
    # source: online shop
    return [makeProduct(
        name = 'chromium picolinate tablets "vitacost"',
        nameShort = 'Cr',
        dataUrl = 'http://www.vitacost.com/vitacost-chromium-picolinate',
        price = 939,
        priceMass = 300, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                chromium = (200, 'mcg')
        )))]

def _iodineTablets():
    # source: online shop
    return [makeProduct(
        name = 'kelp tablets "nature\'s way"',
        nameShort = 'I',
        dataUrl = 'http://www.vitacost.com/natures-way-kelp',
        price = 569,
        priceMass = 180, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                iodine = (400, 'mcg')
        )))]

def _biotinTablets():
    # source: online shop
    return [makeProduct(
        name = 'biotin "source naturals"',
        nameShort = 'biotin',
        dataUrl = 'http://www.vitacost.com/source-naturals-biotin-600-mcg-200-tablets',
        price = 709,
        priceMass = 200, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                biotin = (600, 'mcg')
        )))]

def _molybdenumTablets():
    # source: online shop
    return [makeProduct(
        name = 'molybdenum tablets "kal"',
        nameShort = 'Mo',
        dataUrl = 'http://www.vitacost.com/kal-molybdenum-chelated-250-mcg-100-microtablets',
        price = 499,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                molybdenum = (250, 'mcg')
        )))]

def _potassiumPowder():
    # source: http://www.iherb.com/Now-Foods-Potassium-Chloride-Powder-8-oz-227-g/777
    return [makeProduct(
        name = 'potassium chloride powder "bulk supplements"',
        nameShort = 'K',
        dataUrl = 'http://www.amazon.com/BulkSupplements-Potassium-Chloride-Powder-grams/dp/B00ENS39WG',
        price = 1996,
        **_convert(
            priceMass = (1000, 'g'),
            elementsMass = (1.4, 'g'),
            elements = makeElements(
                potassium = (730, 'mg')
        )))]

def _potassiumTablets():
    # source: online shop
    return [makeProduct(
        name = 'potassium citrate "vitacost"',
        nameShort = 'K2',
        dataUrl = 'http://www.vitacost.com/vitacost-potassium-citrate',
        price = 699,
        priceMass = 300, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                potassium = (99, 'mg')
        )))]

def _floricalTablets():
    # source: online shop
    return [makeProduct(
        name = 'florical tablets "mericon"',
        nameShort = 'F',
        dataUrl = 'http://www.amazon.com/Florical-Calcium-Fluoride-supplements-Industries/dp/B000M4C5TS',
        price = 1359,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                calcium = (145, 'mg'),
                fluoride = (3.75, 'mg')
        )))]

def _calciumTablets():
    res = []

    # source: online shop
    res += [makeProduct(
        name = 'calcium dietary supplement "caltrate"',
        nameShort = 'Ca1',
        price = 1493,
        priceMass = 150, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                calcium = (600, 'mg')
        )))]

    # source: online shop
    res += [makeProduct(
        name = 'ultra calcium with vitamin d3 "vitacost"',
        nameShort = 'Ca2',
        dataUrl = 'http://www.vitacost.com/vitacost-ultra-calcium-1200-mg-with-vitamin-d3-700-iu-per-serving-300-softgels-7',
        price = 1149,
        priceMass = 150, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                energy = (10, 'kcal'),
                fat = (1, 'g'),
                calcium = (1200, 'mg')
        )))]

    return res

def _magnesiumTablets():
    # source: online shop
    return [makeProduct(
        name = 'magnesium tablets "vitacost"',
        nameShort = 'Mg',
        dataUrl = 'http://www.vitacost.com/vitacost-magnesium-400-mg-200-capsules-1',
        price = 649,
        priceMass = 200, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                magnesium = (400, 'mg'),
                magnesiumSup = (400, 'mg')
        )))]

def _ironTablets():
    # source: online shop
    return [makeProduct(
        name = 'iron tablets "nature made"',
        price = 674,
        priceMass = 180, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                iron = (65, 'mg')
        )))]

def _vitaminCTablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin c tablets "vitacost"',
        nameShort = 'vit c',
        dataUrl = 'http://www.vitacost.com/vitacost-vitamin-c-1000-mg-250-capsules',
        price = 1176,
        priceMass = 250, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                vitaminC = (1000, 'mg')
        )))]

def _vitaminKTablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin k tablets "vitacost"',
        nameShort = 'vit k',
        dataUrl = 'http://www.vitacost.com/vitacost-vitamin-k-complex-with-k1-k2-400-mcg-180-softgels',
        price = 2499,
        priceMass = 180, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                vitaminK = (400, 'mcg'),
                vitaminC = (10, 'mg')
        )))]

def _zincTablets():
    # source: online shop
    return [makeProduct(
        name = 'zinc tablets "vitacost"',
        nameShort = 'Zn',
        dataUrl = 'http://www.vitacost.com/vitacost-l-optizinc',
        price = 899,
        priceMass = 200, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                zinc = (30, 'mg')
        )))]

def _riboflavinTablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin b-2 "solgar"',
        nameShort = 'vit b2',
        dataUrl = 'http://www.vitacost.com/solgar-vitamin-b2-riboflavin-50-mg-100-tablets',
        price = 719,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                riboflavin = (50, 'mg')
        )))]

def _vitaminB12Tablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin b-12 tablets "solgar"',
        nameShort = 'vit b12',
        dataUrl = 'http://www.vitacost.com/solgar-vitamin-b12-100-mcg-100-tablets',
        price = 559,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                vitaminB12 = (100, 'mcg')
        )))]

def _vitaminB6Tablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin b-6 "nature\'s way"',
        price = 639,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                carb = (1, 'g'),
                vitaminB6 = (100, 'mg')
        )))]

def _copperTablets():
    # source: online shop
    return [makeProduct(
        name = 'copper tablets "twinlab"',
        price = 621,
        priceMass = 100, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                copper = (2, 'mg')
        )))]

def _vitaminETablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin e "vitacost"',
        nameShort = 'vit e',
        dataUrl = 'http://www.vitacost.com/vitacost-gamma-e-tocopherol-complex-200-iu-60-softgels',
        price = 899,
        priceMass = 60, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                vitaminE = (200, 'IU_vitaminE_d_alphatocopherol'),
                vitaminESup = (200, 'IU_vitaminE_d_alphatocopherol')
        )))]

def _seleniumTablets():
    # source: online shop
    return [makeProduct(
        name = 'hypo-selenium tablets "douglas laboratories"',
        price = 1160,
        priceMass = 90, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                selenium = (200, 'mcg')
        )))]

def _vitaminDTablets():
    # source: online shop
    return [makeProduct(
        name = 'vitamin d "vitacost"',
        nameShort = 'vit d',
        dataUrl = 'http://www.vitacost.com/vitacost-vitamin-d3-as-cholecalciferol-1000-iu-200-capsules-1',
        price = 599,
        priceMass = 200, # tablets
        elementsMass = 1,
        **_convert(
            elements = makeElements(
                vitaminD = (1000, 'IU_vitaminD')
        )))]
