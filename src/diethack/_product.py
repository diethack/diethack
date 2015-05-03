from _elements import makeElements, makeElementsUnits
import logging

MASS_MAX = 10000 # don't want to eat something >10kg per day...

def makeProduct(name, elementsMass, elements, price=0, priceMass=100,
                massLimit = [0, MASS_MAX], dataUrl='', refusePercent=0,
                refuseDesc = '', nameShort=''):
    return {'name': name,
            'nameShort': nameShort,
            'dataUrl': dataUrl,
            'price': price,
            'priceMass': priceMass,
            'massLimit': massLimit,
            'elementsMass': elementsMass,
            'elements': elements,
            'refusePercent': refusePercent,
            'refuseDesc': refuseDesc}

def makeProductUnits():
    return makeProduct(
            name = None,
            dataUrl = None,
            price = 'cnt',
            priceMass = 'g',
            massLimit = 'g',
            elementsMass = 'g',
            elements = makeElementsUnits())
