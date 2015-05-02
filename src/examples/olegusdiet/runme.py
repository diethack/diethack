import logging
from random import seed, sample
from goal import goal
from products import products
from diethack import makeProduct, makeElements, makeProductUnits, \
                     fetchNndb, fetchNndbCodes, solve, makeConverter, \
                     reportHtml, reportShop, reportTxt

def randomProducts(count):
    fetch = lambda c: \
        makeConverter().convertDict(fetchNndb(c), makeProductUnits())
    return [
        makeProduct(**dict(fetch(c).items() + [('price',10), ('priceMass',1)]))
           for c in sample(fetchNndbCodes(), count)]

def elementsPriority():
    return dict([(k, 1) for k in makeElements().keys()])

if __name__ == '__main__':
    seed(12345)
    logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    olegusProds = products()
    randomProds = randomProducts(20)

    olegusDiet = solve(olegusProds, goal(), elementsPriority())
    randomDiet = solve(randomProds, goal(), elementsPriority())

    with open('olegusdiet.html', 'w') as f:
        f.write(reportHtml(olegusProds, makeProductUnits(), goal(),
                           olegusDiet, 'light'))
    with open('olegusdiet.txt', 'w') as f:
        f.write(reportTxt(olegusProds, makeProductUnits(), goal(), olegusDiet))
    with open('olegusdiet-shoplist.html', 'w') as f:
        f.write(reportShop(olegusProds, makeProductUnits(), goal(),
                           olegusDiet, 'light'))
    with open('randomdiet.html', 'w') as f:
        f.write(reportHtml(randomProds, makeProductUnits(), goal(),
                           randomDiet, 'light'))
