from _util import call, roughlyLessEqual, roughlyGreaterEqual, htmlEscape
from pprint import pformat
import operator

def prettify(table):
    padding = []
    for i in xrange(max([len(x) for x in table])):
        padding.append(max([len(x[i]) for x in table if i < len(x)]))
    return '\n'.join([' '.join([col.ljust(pad)
                                for col, pad in zip(row, padding)])
                      for row in table])

def reportTxt(ps, units, goal, sln):
    res = []
    pms = sln['masses']
    shifts = sln['shifts']
    res.append(prettify(
        [[ps[i]['name'],
          '%i g' % pms[i],
          '(%i cnt)' % ((pms[i] * ps[i]['price']) / ps[i]['priceMass'])]
          for i in xrange(len(ps)) if pms[i] > 0]))
    res.append('')
    res.append(prettify(
        [['mass',
          '%i %s' % (sum(pms), units['elementsMass'])],
         ['price',
          '%i %s' % (sum([pms[i] * ps[i]['price'] / ps[i]['priceMass']
                          for i in xrange(len(ps))]),
                     units['price'])]] +
        [[k,
          '%i %s%s' % (sum([pms[i]*ps[i]['elements'][k]/ps[i]['elementsMass']
                            for i in xrange(len(ps))]),
                       ('(%+i) ' % -shifts[k]) if shifts[k] else '',
                       v)] for k, v in sorted(units['elements'].items())]))
    res.append('')
    return '\n'.join(res)

def makeStyle(theme):
    return {'light': makeStyleColorsLight(),
            'dark': makeStyleColorsDark()
           }[theme] + makeStyleShapes()

def makeStyleColorsLight():
    return [
        ':root {',
        '    background-color: #ffffff;',
        '    color: #000000;',
        '}',
        '.attention {',
        '    color: #960018;',
        '}',
        'table.data tr:not(:last-of-type) td {',
        '    border-color: #a0a0a0;',
        '}',
        'table.data th {',
        '    background-color: #a0a0a0;',
        '}',
        'table.data tr:nth-of-type(even) td {',
        '    background-color: #e9e9e9;',
        '}',
    ]

def makeStyleColorsDark():
    return [
        ':root {',
        '    background-color: #000000;',
        '    color: #ffffff;',
        '}',
        '.attention {',
        '    color: #ff6981;',
        '}',
        'table.data tr:not(:last-of-type) td {',
        '    border-color: #404040;',
        '}',
        'table.data th {',
        '    background-color: #404040;',
        '}',
        'table.data tr:nth-of-type(even) td {',
        '    background-color: #101010;',
        '}',
    ]

def makeStyleShapes():
    return [
        ':root {',
        '    font-size: 0.9em;',
        '}',
        'a {',
        '    text-decoration: underscore;',
        '    color: inherit;',
        '}',
        '.attention {',
        '    font-weight: bold;',
        '}',
        'table, td, th {',
        '    border-spacing: 0;',
        '    padding: 0;',
        '}',
        'table.data {',
        '    margin: 0;',
        '}',
        'table.data td {',
        '    padding-top: 0.25rem;',
        '    padding-bottom: 0.25rem;',
        '    white-space: nowrap;',
        '}',
        'table.data tr:not(:last-of-type) td {',
        '    border-bottom-style: solid;',
        '    border-bottom-width: 0.1rem;',
        '}',
        'table.data th {',
        '    margin: 0;',
        '    padding-top: 0.75rem;',
        '    padding-bottom: 0.75rem;',
        '    font-size: 1rem;',
        '    font-weight: bold;',
        '    text-align: left;',
        '}',
        'table.data thead th {',
        '    vertical-align: top;',
        '}',
        'table.data tfoot th {',
        '    vertical-align: bottom;',
        '}',
        'table.data td, table.data th {',
        '    padding-left: 0.75rem;',
        '    padding-right: 0.75rem;',
        '}',
        'table.data td:last-of-type, table.data th:last-of-type {',
        '    text-align: right;',
        '}'
    ]

def productName(p):
    return htmlEscape(p['nameShort'] if p['nameShort'] else p['name'])

def makeHeadProducts(ps):
    return reduce(operator.add, [[
         '<th title="%s">' % htmlEscape(p['name'])
         ] + ([
         '    <a href="%s">' % p['dataUrl'],
         '        ' + productName(p),
         '    </a>']
         if p['dataUrl'] else [
         '    ' + productName(p)]) + [
         '</th>'
        ] for p in ps
    ])

def makeHeadRows(ps):
    return list([
        '<tr>',
        '    <th>',
        '        element',
        '    </th>',
        '    <th>',
        '        units',
        '    </th>',
        '    <th>',
        '        total',
        '    </th>',
        '    <th>',
        '        lower bound',
        '    </th>',
        '    <th>',
        '        upper bound',
        '    </th>'] +
       ['    ' + s for s in makeHeadProducts(ps)] + [
        '    <th>',
        '        element',
        '    </th>',
        '</tr>'
    ])

def makeFootRows(ps):
    return makeHeadRows(ps)

def wholeMass(i, ps, sln):
    return sln['masses'][i] * 100.0 / (100.0 - ps[i]['refusePercent'])

def refuseMass(i, ps, sln):
    return wholeMass(i, ps, sln) * ps[i]['refusePercent'] / 100.0

def wholeMasses(ps, sln):
    return [wholeMass(i, ps, sln) for i in xrange(len(ps))]

def refuseMasses(ps, sln):
    return [refuseMass(i, ps, sln) for i in xrange(len(ps))]

def productCost(i, ps, sln):
    return sln['masses'][i] * ps[i]['price'] / ps[i]['priceMass']

def productsCosts(ps, sln):
    return [productCost(i, ps, sln) for i in xrange(len(ps))]

def productElement(i, k, ps, sln):
    return sln['masses'][i] * ps[i]['elements'][k] / ps[i]['elementsMass']

def productsElements(k, ps, sln):
    return [productElement(i, k, ps, sln) for i in xrange(len(ps))]

def makeRoundNumber(num):
    if num >= 10.0:
        return '%i' % round(num)
    if num >= 1.0:
        return '%.1f' % num
    elif num >= 0.01:
        return '%.2f' % num
    elif num >= 0.000001:
        return '%.1e' % num
    else:
        return str(0)

def makeNumber(num):
    return '<span title="%e">%s</span>' % (num, makeRoundNumber(num))

def makeBodyTotalCost(ps, sln):
    return makeNumber(sum(productsCosts(ps, sln)))

def makeBodyTotalElement(k, ps, sln):
    return makeNumber(sum(productsElements(k, ps, sln)))

def makeBodyMassProducts(ps, sln):
    mmax = max(wholeMasses(ps, sln))
    return reduce(operator.add, [[
        '<td class="attention">',
        '    ' + makeNumber(wholeMass(i, ps, sln)),
        '</td>'
        ] if wholeMass(i, ps, sln) == mmax else [
        '<td>',
        '    ' + makeNumber(wholeMass(i, ps, sln)),
        '</td>'
        ] for i in xrange(len(ps))
    ])

def makeBodyMass(ps, units, sln):
    return list([
        '<td>',
        '    mass with refuse',
        '</td>',
        '<td>',
        '    ' + units['elementsMass'],
        '</td>',
        '<td>',
        '    ' + makeNumber(sum(wholeMasses(ps, sln))),
        '</td>',
        '<td>',
        '    -',
        '</td>',
        '<td>',
        '    -',
        '</td>'] +
        makeBodyMassProducts(ps, sln) + [
        '<td>',
        '    mass with refuse',
        '</td>'
    ])

def makeBodyMassRefuseProducts(ps, sln):
    mmax = max(refuseMasses(ps, sln))
    return reduce(operator.add, [[
        '<td class="attention">',
        '    ' + makeNumber(refuseMass(i, ps, sln)),
        '</td>'
        ] if refuseMass(i, ps, sln) == mmax  and mmax != 0 else [
        '<td>',
        '    ' + makeNumber(refuseMass(i, ps, sln)),
        '</td>'
        ] for i in xrange(len(ps))
    ])

def makeBodyMassRefuse(ps, units, sln):
    return list([
        '<td>',
        '    refuse mass',
        '</td>',
        '<td>',
        '    ' + units['elementsMass'],
        '</td>',
        '<td>',
        '    ' + makeNumber(sum(refuseMasses(ps, sln))),
        '</td>',
        '<td>',
        '    -',
        '</td>',
        '<td>',
        '    -',
        '</td>'] +
        makeBodyMassRefuseProducts(ps, sln) + [
        '<td>',
        '    refuse mass',
        '</td>'
    ])

def makeBodyCostProducts(ps, sln):
    cmax = max(productsCosts(ps, sln))
    return reduce(operator.add, [[
        '<td class="attention">',
        '    ' + makeNumber(c),
        '</td>'
        ] if c == cmax and c != 0 else [
        '<td>',
        '    ' + makeNumber(c),
        '</td>'
        ] for i in xrange(len(ps))
          for c in [productCost(i, ps, sln)]
    ])

def makeBodyCost(ps, units, sln):
    return list([
        '<td>',
        '    cost',
        '</td>',
        '<td>',
        '    ' + units['price'],
        '</td>',
        '<td>',
        '    ' + makeBodyTotalCost(ps, sln),
        '</td>',
        '<td>',
        '    -',
        '</td>',
        '<td>',
        '    -',
        '</td>'] +
        makeBodyCostProducts(ps, sln) + [
        '<td>',
        '    cost',
        '</td>'
    ])

def elementInBounds(k, ps, goal, sln):
    total = sum(productsElements(k, ps, sln))
    return roughlyLessEqual(min(goal[k]), total) \
       and roughlyGreaterEqual(max(goal[k]), total)

def makeBodyElementTotal(k, ps, goal, sln):
    return list([
        '<span%s>' % (''
                      if elementInBounds(k, ps, goal, sln) else
                      ' class="attention"'),
        '    ' + makeBodyTotalElement(k, ps, sln),
        '</span>'
    ])

def makeBodyElement(k, ps, units, goal, sln):
    total = sum(productsElements(k, ps, sln))
    return list([
        '<td>',
        '    ' + k,
        '</td>',
        '<td>',
        '    ' + units['elements'][k],
        '</td>',
        '<td>'] + 
       ['    ' + s for s in makeBodyElementTotal(k, ps, goal, sln)] + [
        '</td>',
        '<td class="attention">'
        if roughlyLessEqual(total, min(goal[k])) else
        '<td>',
        '    ' + makeNumber(min(goal[k])),
        '</td>',
        '<td class="attention">'
        if roughlyGreaterEqual(total, max(goal[k])) else
        '<td>',
        '    ' + makeNumber(max(goal[k])),
        '</td>'] +
        makeBodyElementProducts(k, ps, sln) + [
        '<td>',
        '    ' + k,
        '</td>'
    ])

def makeBodyElementProducts(k, ps, sln):
    xmax = max(productsElements(k, ps, sln))
    return reduce(operator.add, [[
        '<td',
        '    class="attention"' if x == xmax and x != 0 else '',
        '>',
        '    ' + makeNumber(x),
        '</td>'
        ] for i in xrange(len(ps))
          for x in [productElement(i, k, ps, sln)]
    ])

def makeBodyRowsElements(ps, units, goal, sln):
    return reduce(operator.add, [[
        '<tr>'] +
       ['    ' + s for s in makeBodyElement(k, ps, units, goal, sln)] + [
        '</tr>'
       ] for k in sorted(units['elements'].keys())
    ])

def makeBodyRows(ps, units, goal, sln):
    return list([
            '<tr>'] +
           ['    ' + s for s in makeBodyMass(ps, units, sln)] + [
            '</tr>',
            '<tr>'] +
           ['    ' + s for s in makeBodyMassRefuse(ps, units, sln)] + [
            '</tr>',
            '<tr>'] +
           ['    ' + s for s in makeBodyCost(ps, units, sln)] + [
            '</tr>'] +
            makeBodyRowsElements(ps, units, goal, sln)
    )

def makeProductsTable(ps, units, goal, sln):
    return list([
        '<table class="data" summary="none">',
        '    <thead>'] +
       ['        ' + s for s in makeHeadRows(ps)] + [
        '    </thead>',
        '    <tbody>'] +
       ['        ' + s for s in makeBodyRows(ps, units, goal, sln)] + [
        '    </tbody>',
        '    <tfoot>'] +
       ['        ' + s for s in makeFootRows(ps)] + [
        '    </tfoot>',
        '</table>'
    ])

def makeShopBodyRows(ps, units, goal, sln):
    return reduce(operator.add, [[
        '<tr>',
        '    <td>',
        '        <a href="%s">' % ps[i]['dataUrl'],
        '            ' + htmlEscape(ps[i]['name']),
        '        </a>',
        '    </td>',
        '    <td>',
        '        %s' % makeNumber(sln['masses'][i]),
        '    </td>',
        '    <td>',
        '        %s' % makeNumber(ps[i]['price']),
        '    </td>',
        '    <td>',
        '        %s' % makeNumber(ps[i]['priceMass']),
        '    </td>',
        '</tr>'
        ] for i in xrange(len(ps))])

def makeShopTable(ps, units, goal, sln):
    return list([
        '<table class="data" summary="none">',
        '    <thead>',
        '        <tr>',
        '            <th>product</th>',
        '            <th>mass (%s)</th>' % units['elementsMass'],
        '            <th>cost (%s)</th>' % units['price'],
        '            <th>cost mass (%s)</th>' % units['priceMass'],
        '        </tr>',
        '    </thead>',
        '    <tbody>'] +
       ['        ' + s for s in makeShopBodyRows(ps, units, goal, sln)] + [
        '    </tbody>',
        '    <tfoot>',
        '        <tr>',
        '            <th>product</th>',
        '            <th>mass (%s)</th>' % units['elementsMass'],
        '            <th>cost (%s)</th>' % units['price'],
        '            <th>cost mass (%s)</th>' % units['priceMass'],
        '        </tr>',
        '    </tfoot>',
        '</table>'
    ])

def makeHtml(style, body):
    return list([
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"',
        '"http://www.w3.org/TR/html4/strict.dtd">',
        '',
        '<html lang="en">',
        '<head>',
        '    <title></title>',
        '    <meta http-equiv="Content-Type" content="text/html; '
             'charset=utf-8">',
        '    <meta http-equiv="Content-Style-Type" content="text/css">',
        '    <style type="text/css">'] +
       ['        ' + s for s in style] + [
        '    </style>',
        '</head>',
        '<body>'] +
       ['    ' + s for s in body] + [
        '</body>'
        ''
    ])

def activeProducts(ps, sln):
    return [ps[i] for i in xrange(len(ps)) if sln['masses'][i] > 0]

def activeSolution(sln):
    return {'masses': [m for m in sln['masses'] if m > 0],
            'shifts': sln['shifts']}

def reportHtml(ps, units, goal, sln, theme):
    return '\n'.join(makeHtml(makeStyle(theme), makeProductsTable(
        activeProducts(ps, sln), units, goal, activeSolution(sln))))

def reportShop(ps, units, goal, sln, theme):
    return '\n'.join(makeHtml(makeStyle(theme), makeShopTable(
        activeProducts(ps, sln), units, goal, activeSolution(sln))))
