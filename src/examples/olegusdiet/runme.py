from goal import goal
from products import products
from diethack import makeProduct, makeElements, makeProductUnits
from random import seed
import logging

def randomProducts(count):
    return [makeProduct(**dict(p.items() + [('price',10), ('priceMass',1)]))
           for p in sample(fetchUsdaCodes(), count)]

def elementsPriority():
    return dict([(k, 1) for k in makeElements().keys()])

if __name__ == '__main__':
    seed()
    logging.basicConfig(format='%(levelname)-8s %(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    myDiet = solve(products(), goal(), elementsPriority())
    randomDiet = solve(randomProducts(20), goal(), elementsPriority())

    with open('mydiet.html', 'w') as f:
        f.write(reportHtml(products(), makeProductUnits(), goal(),
                           myDiet, 'light'))
    with open('mydiet.txt', 'w') as f:
        f.write(reportTxt(products(), makeProductUnits(), goal(), myDiet))
    with open('mydiet-shoplist.html', 'w') as f:
        f.write(reportShop(products(), makeProductUnits(), goal(),
                           myDiet, 'light'))
    with open('randomdiet.html', 'w') as f:
        f.write(reportHtml(products(), makeProductUnits(), goal(),
                           randomDiet, 'light'))
