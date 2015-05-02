from goal import goal
from products import products
from diethack import makeProduct, makeElements, makeProductUnits, \
                     fetchNndbCodes, solve
from random import seed
import logging

def randomProducts(count):
    return [makeProduct(**dict(p.items() + [('price',10), ('priceMass',1)]))
           for p in sample(fetchNndbCodes(), count)]

def elementsPriority():
    return dict([(k, 1) for k in makeElements().keys()])

if __name__ == '__main__':
    seed(12345)
    logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    olegusDiet = solve(products(), goal(), elementsPriority())
    randomDiet = solve(randomProducts(20), goal(), elementsPriority())

    with open('olegusdiet.html', 'w') as f:
        f.write(reportHtml(products(), makeProductUnits(), goal(),
                           olegusDiet, 'light'))
    with open('olegusdiet.txt', 'w') as f:
        f.write(reportTxt(products(), makeProductUnits(), goal(), olegusDiet))
    with open('olegusdiet-shoplist.html', 'w') as f:
        f.write(reportShop(products(), makeProductUnits(), goal(),
                           olegusDiet, 'light'))
    with open('randomdiet.html', 'w') as f:
        f.write(reportHtml(products(), makeProductUnits(), goal(),
                           randomDiet, 'light'))
