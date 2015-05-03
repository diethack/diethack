from _util import call
from os import path, remove, close
from os.path import dirname
from tempfile import mkstemp
import operator
import logging

GLPSOL_EXEC = 'glpsol'
RELAX = 0.01
FLOAT_FMT = '%.16e'
THRESH = 1e-6

def solve(products, goal, prior):
    emax = dict([(k, max([unitElementMass(p, k) for p in products]))
                          for k in goal.keys()])
    emax = dict([(k, v if v > THRESH else 1.0) for k, v in emax.items()])
    logging.debug('emax = %s' % emax)
    normShiftsVals = glpkSolve(generateShifts(products, goal, prior, emax))
    normShifts = dict(zip(sorted(goal.keys()), normShiftsVals))
    return {
        'shifts': dict([(k, v*emax[k]) for k, v in normShifts.items()]),
        'masses': glpkSolve(generate(products, goal, prior, normShifts, emax))}

def generateShifts(ps, goal, prior, emax):
    return '\n'.join(
        makeHeader()
        + [''] + makeVarMass(ps)
        + [''] + makeVarShift(goal)
        + [''] + makeMinimizeShift(goal, prior, emax)
        + [''] + makeConstrMassShiftDynamic(ps, goal, prior, emax)
        + [''] + makeConstrMassLimits(ps)
        + [''] + makeSolve()
        + [''] + makePrintShifts(goal)
        + [''] + makeEnd()
    )

def generate(ps, goal, prior, shifts, emax):
    return '\n'.join(
        makeHeader()
        + [''] + makeVarMass(ps)
        + [''] + makeMinimizeCost(ps)
        + [''] + makeConstrMassShiftStatic(ps, goal, prior, shifts, emax)
        + [''] + makeConstrMassLimits(ps)
        + [''] + makeSolve()
        + [''] + makePrintMasses(ps)
        + [''] + makeEnd()
    )

def glpkSolve(model):
    logging.debug('GLPK input:\n%s' % model)
    fd, fname = mkstemp('.mod')
    close(fd)
    with open(fname, 'w') as f:
        f.write(model)
    try:
        sln = call(' '.join([GLPSOL_EXEC, '--model', fname]), dirname(fname))
    finally:
        remove(fname)
    logging.debug('GLPK output:\n%s' % sln)
    sln = sln.split('$begin$')
    if len(sln) == 1:
        raise Exception('cannot solve: %s' % str(sln[0]))
    sln = sln[1].split('$end$')[0]
    res = []
    for v in sln.split(';'):
        try:
            res.append(float(v))
        except ValueError:
            break
    return res

def makeHeader():
    return ['/* autogenerated */']

def makeVarMass(ps):
    return ['var mass%i >= 0;' % i for i in xrange(len(ps))]

def makeVarShift(goal):
    res = []
    res += ['var shiftPos_%s >= 0;' % k for k in goal.keys()]
    res.append('')
    res += ['var shiftNeg_%s >= 0;' % k for k in goal.keys()]
    return res

def preciseStr(f):
    return FLOAT_FMT % f

def makeMinimizeShift(goal, rawPrior, emax):
    prior = dict([(k, v*emax[k]) for k, v in rawPrior.items()])
    maxPrior = max(prior.values())
    shift = ' + '.join(['((shiftPos_%s + shiftNeg_%s) * %s)'
                        % (k, k, preciseStr(float(prior[k])/maxPrior))
                        for k in goal.keys()])
    return ['minimize shift: %s;' % shift]

def makeMinimizeCost(ps):
    cost = ' + '.join(['(mass%i * %s)' % (i, preciseStr(unitPrice(ps[i])))
                       for i in xrange(len(ps))])
    return ['minimize cost: %s;' % cost]

def unitElementMass(p, k):
    return float(p['elements'][k]) / p['elementsMass']

def unitPrice(p):
    return float(p['price']) / p['priceMass']

def makeConstr(name, lim, body, div=1):
    return ['subject to %s: %s <= %s <= %s;'
            % (name, preciseStr(float(min(lim))/div),
               body, preciseStr(float(max(lim))/div))]

def makeSumMass(ps, k, div):
    return ' + '.join(['(mass%i * %s)'
                       % (i, preciseStr(unitElementMass(ps[i], k)/div))
                       for i in xrange(len(ps))])

def makeShiftDynamic(k, scale):
    return '((shiftPos_%s - shiftNeg_%s)*%s)' % (k, k, preciseStr(scale))

def makeConstrMassLimits(ps):
    return reduce(operator.add,
        [makeConstr('massLimit%i' % i, ps[i]['massLimit'], 'mass%i' % i)
         for i in xrange(len(ps))])

def makeConstrMassShiftDynamic(ps, goal, prior, emax):
    return reduce(operator.add,
        [makeConstr('%s_lo' % k, v, '%s + %s' % (makeSumMass(ps, k, emax[k]),
                    makeShiftDynamic(k, 1-RELAX)), emax[k]) + \
         makeConstr('%s_hi' % k, v, '%s + %s' % (makeSumMass(ps, k, emax[k]),
                    makeShiftDynamic(k, 1+RELAX)), emax[k])
         for k, v in goal.items()
         if prior[k] > 0])

def makeConstrMassShiftStatic(ps, goal, prior, shifts, emax):
    return reduce(operator.add,
        [makeConstr('%s' % k, v, '%s + %s' % (makeSumMass(ps, k, emax[k]),
                                              preciseStr(shifts[k])),
                    emax[k])
         for k, v in goal.items()
         if prior[k] > 0])

def makeSolve():
    return ['solve;']

def makePrint(exprs):
    return \
        ["printf: '$begin$';"] + \
        ["printf: '%s;', %s;" % (FLOAT_FMT, x) for x in exprs] + \
        ["printf: '$end$';"]

def makePrintShifts(goal):
    return makePrint(['shiftPos_%s - shiftNeg_%s'
                      % (k, k) for k in sorted(goal.keys())])

def makePrintMasses(ps):
    return makePrint(['mass%i' % i for i in xrange(len(ps))])

def makeEnd():
    return ['end;']
