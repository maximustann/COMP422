import operator
import math
import random
import sys
import numpy

sys.path.append("../deap")
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
#pset.addEphemeralConstant("rand101", lambda: random.randint(0,9))
pset.renameArguments(ARG0='x0')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual, points_neg, points_pos):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : 

    sqerrors_1 = [(func(x) - (1. / x) + math.sin(x))**2 for x in points_pos]
    sqerrors_2 = [(func(x) - 2. * x + x ** 2. + 3.)**2 for x in points_neg]
    sqerrors = [sqerrors_1[i] + sqerrors_2[i] for i in range(5)]
    #if math.fsum(sqerrors) / (len(points_neg) +len(points_pos)) < 1:
        #print individual
        #print 
    return math.fsum(sqerrors) / (len(points_neg) +len(points_pos)),

toolbox.register("evaluate", evalSymbReg, points_neg = [x for x in range(-5,0)], points_pos = [x  for x in range(1, 6)])
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    #random.seed(318)

    pop = toolbox.population(n=40)
    hof = tools.HallOfFame(1)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.6, 0.1, 50, stats=mstats,
                                   halloffame=hof, verbose=True)
    # print log
    print hof[0]
    return pop, log, hof

if __name__ == "__main__":
    main()
