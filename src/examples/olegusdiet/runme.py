from goal import goal
from products import products
from elements import priorities
from diethack import makeProduct

def randomProducts(count):
    return [makeProduct(**dict(p.items() + [('price', 10), ('priceMass', 1)]))
           for p in sample(fetchUsdaCodes(), count)]

if __name__ == '__main__':
    myDiet = solve(products(), goal(), priorities())
    randomDiet = solve(randomProducts(100), goal(), priorities())
