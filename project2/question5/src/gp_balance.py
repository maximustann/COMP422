import operator
import math
import random
import sys
import numpy
import os
import csv

sys.path.append("../deap")
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


data = numpy.genfromtxt('./data/balance.data', delimiter = ',')
best_fitness = 0.0
# Define new functions
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 4)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addPrimitive(operator.abs, 1)

pset.addTerminal(1)
pset.addTerminal(2)
pset.addTerminal(3)
pset.addTerminal(4)
pset.addTerminal(5)
pset.addTerminal(6)
pset.addTerminal(7)
pset.addTerminal(8)
pset.addTerminal(9)
#we got thirdteen features
pset.renameArguments(ARG0='x0')
pset.renameArguments(ARG1='x1')
pset.renameArguments(ARG2='x2')
pset.renameArguments(ARG3='x3')

creator.create("FitnessMin", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalSymbReg(individual):
    global best_fitness
    func = toolbox.compile(individual)
    result_list = []
    fitness = 0.0
    line_res = 0
    length = len(data)
    for pointer in range(len(data)):
        line_result = []
        var0 = data[pointer][0]
        var1 = data[pointer][1]
        var2 = data[pointer][2]
        var3 = data[pointer][3]
        classes = data[pointer][4]
        line_result.append(func(var0, var1, var2, var3))
        line_result.append(classes)
        result_list.append(line_result)

    #print result_list
    mean_var = []
    for i in range(1, 4):
        mean = cal_mean(result_list, i)
        std_var = std(result_list, mean, i)
        mean_var.append([mean, std_var])
        if std_var == 0:
            return -1,

    for dataline in result_list:
        if dataline[1] == distributor(mean_var, dataline[0]):
            fitness += 1.0
    fitness /= len(result_list)
    if fitness > best_fitness:
        best_fitness = fitness
        write_file(result_list)
    return fitness,

toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize = 3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mate", gp.staticLimit(operator.attrgetter('height'), 20))
toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter('height'), 20))

def write_file(dataset):
    title = ["feature", "class"]
    if not os.path.exists("wine_new_feature.csv"):
        fd = open("./result/balance_new_feature.csv", 'w')
        writer = csv.writer(fd)
        writer.writerow(title)
        for line in dataset:
            writer.writerow(line)
    else:
        fd = open("./result/balance_new_feature.csv", 'w')
        fd.truncate(0)
        writer = csv.writer(fd)
        writer.writerow(title)
        for line in dataset:
            writer.writerow(line)
def cal_mean(result_list, class_label):
    summ = 0.0
    for item in result_list:
        if item[1] != class_label:
            continue
        summ += item[0]
    mean = summ / len(result_list)
    return mean

def std(result_list, mean, class_label):
    summ = 0.0
    for item in result_list:
        if item[1] != class_label:
            continue
        summ += (item[0] - mean) ** 2
    summ /= len(result_list)
    return math.sqrt(summ)

def _compare(res):
    items = res.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort(reverse=True)
    return float(backitems[0][1][-1])

def guassian(mean, var, value):
    w = 1 / math.sqrt(2 * math.pi * var)
    k = math.exp(0.5 * (-math.pow((value - mean), 2) / (2 * var)))
    return w * k

def probability_cal(class_data, dataline):
    pros = guassian(class_data[0], class_data[1], dataline)
    return pros

def distributor(mean_var, dataline):
    class1_data = mean_var[0]
    class2_data = mean_var[1]
    class3_data = mean_var[2]

    res = {}
    res["class1"] = probability_cal(class1_data, dataline)
    res["class2"] = probability_cal(class2_data, dataline)
    res["class3"] = probability_cal(class3_data, dataline)
    return _compare(res)


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

    pop, log = algorithms.eaSimple(pop, toolbox, 0.6, 0.1, 300, stats=mstats,
                                   halloffame=hof, verbose=True)
    print hof[0]
    return pop, log, hof

if __name__ == "__main__":
    main()
