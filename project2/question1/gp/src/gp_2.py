#!/bin/env python
import array
import random
import operator
import sys
import numpy
import csv
import os


sys.path.append("../../deap")
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

pset = gp.PrimitiveSet("MAIN", 2)
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)
pset.addTerminal(True)
pset.addTerminal(False)
pset.renameArguments(ARG0="x")
pset.renameArguments(ARG1="y")

creator.create("FitnessMax", base.Fitness, weights = (4, ))
creator.create("Individual", gp.PrimitiveTree, fitness = creator.FitnessMax,
                pset = pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset = pset, min_ = 1, max_ = 6)#generate individual tree
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset = pset)
def fitness_function(individual):
    result = 0
    func = toolbox.compile(individual)
    if func(0, 0) == 0:
        result += 1
    if func(1, 1) == 0:
        result += 1
    if func(1, 0) == 1:
        result += 1
    if func(0, 1) == 1:
        result += 1
    #print result
    return result,

toolbox.register("evaluate", fitness_function)
toolbox.register("select", tools.selRoulette)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_ = 1, max_ = 6)
toolbox.register("mutate", gp.mutUniform, expr = toolbox.expr_mut, pset = pset)

def gp(generation, number, cross_rate, mutate_rate):
    generation += 1
    pop = toolbox.population(number)
    for individual in pop:
        individual.fitness.values = toolbox.evaluate(individual)
    selected = toolbox.select(pop, 15)
    offspring = [toolbox.clone(ind) for ind in selected]
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < cross_rate:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random < mutate_rate:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit 
    pop[:] = offspring
    return pop, generation
def evaluate(pop):
    judge, child = __stoping_criteria(pop)
    if judge:
        return child
    return False

def __stoping_criteria(pop):
    children = []
    for i, child in enumerate(pop):
        if child.fitness.values[0] == 4:
            print child 
            return True, child
    return False, []
def main(population, crossrate, mutation_rate):
    popu, generation = gp(0, population, crossrate, mutation_rate)

    while True:
        child =  evaluate(popu)
        if child is not False:
            break
        popu, generation = gp(generation, population, crossrate, mutation_rate)

    return child, generation

def write_file(result, filename, title):
    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(title)
        for i in range(len(result)):
            write.writerow(result[i])

def paste(filename_1, filename_2, newfile):
    os.system("paste %s %s > %s" % (filename_1, filename_2, newfile))
    os.system("rm %s %s" % (filename_1, filename_2))

if __name__ == "__main__":

    round_ = 20
    population = 20
    crossrate = 0.6
    mutation_rate = 0.02
    result = []
    for i in range(round_):
        child, generation = main(population, crossrate, mutation_rate)
        #result[str(child)] = generation
        result.append([generation])
    write_file(result, "./data/large_tree.csv", ["large_tree"])

