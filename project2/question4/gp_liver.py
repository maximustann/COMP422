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

data = numpy.genfromtxt('liver.data', delimiter = ',')

# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 6)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.abs, 1)
pset.addPrimitive(operator.pow, 2)
#pset.addPrimitive(operator.neg, 1)
#pset.addPrimitive(math.cos, 1)
#pset.addPrimitive(math.sin, 1)

pset.addTerminal(0)
pset.addTerminal(1)
pset.addTerminal(2)
pset.addTerminal(3)
pset.addTerminal(4)
pset.addTerminal(5)
pset.addTerminal(6)
pset.addTerminal(7)
pset.addTerminal(8)
pset.addTerminal(9)
#pset.addEphemeralConstant("rand101", lambda: random.randint(0,9))
#we got six features
pset.renameArguments(ARG0='x0')
pset.renameArguments(ARG1='x1')
pset.renameArguments(ARG2='x2')
pset.renameArguments(ARG3='x3')
pset.renameArguments(ARG4='x4')
pset.renameArguments(ARG5='x5')

creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual):
    func = toolbox.compile(individual)
    fitness = 0
    line_res = 0
    length = len(data)
    for pointer in range(len(data)):
        var0 = data[pointer][0]
        var1 = data[pointer][1]
        var2 = data[pointer][2]
        var3 = data[pointer][3]
        var4 = data[pointer][4]
        var5 = data[pointer][5]
        var6 = data[pointer][6]
        line_res = func(var0, var1, var2, var3, var4, var5)
        if line_res > 0:
            if var6 == 1:
                fitness += 1.0 / length
        else:
            if var6 == 2:
                fitness += 1.0 / length
    return fitness,

toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize = 3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(operator.attrgetter('height'), 20))
toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter('height'), 20))


def main():

    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.6, 0.1, 200, stats=mstats,
                                   halloffame=hof, verbose=True)
    print hof[0]
    return pop, log, hof

if __name__ == "__main__":
    main()
