import time
from logger import Logger
from solution import Solution
import objects

class Solver(object):
    def __init__(self):
        logFields = []
        logFields.append({'id':'elapTime',   'name':'Elap. Time (s)', 'headerformat':'{:>14s}', 'valueformat':'{:>14.8f}'})
        logFields.append({'id':'objValue',   'name':'Obj. Value',     'headerformat':'{:>10s}', 'valueformat':'{:>10.8f}'})
        logFields.append({'id':'iterations', 'name':'Iterations',   'headerformat':'{:>12s}', 'valueformat':'{:>12d}'})
        self.logger = Logger(fields=logFields)
        self.logger.printHeaders()
    
    def startTimeMeasure(self):
        self.startTime = time.time()
    
    def writeLogLine(self, objValue, iterations):
        logValues = { }
        logValues['elapTime'] = time.time() - self.startTime
        logValues['objValue'] = objValue
        logValues['iterations'] = iterations
        self.logger.printValues(logValues)
    
    def solve(self, config, problem):
        self.startTimeMeasure()
        self.writeLogLine(float('infinity'), 0)

        solution, elapsedEvalTime, evaluatedCandidates = self.greedyConstruction(config, problem)
        self.writeLogLine(solution.cost, 1)

        #localSearch = LocalSearch(config)
        #solution = localSearch.run(solution)

        self.writeLogLine(solution.cost, 1)
        
        avg_evalTimePerCandidate = 0.0
        if (evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * elapsedEvalTime / float(evaluatedCandidates)

        print ('')
        print ('Greedy Candidate Evaluation Performance:')
        print ('  Num. Candidates Eval.', evaluatedCandidates)
        print ('  Total Eval. Time     ', elapsedEvalTime, 's')
        print ('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')
        
        #localSearch.printPerformance()
        
        return(solution)

    def greedyConstruction(self, config, problem):
        # get an empty solution for the problem
        solution = Solution.createEmptySolution(config, problem)
        
        # get tasks and sort them by their total required resources in descending order
        services = problem.services
        sortedServices = sorted(services, key=lambda service: service.startingTime, reverse=False)
        
        elapsedEvalTime = time.time()
        evaluatedCandidates = 0
        
        # for each task taken in sorted order
        nBusesUtilised = 0
        busesUtilised = set()

        for s in sortedServices:
            #costB = list()

            busUtilised, evalc = self.getBestBus(s, busesUtilised, problem, nBusesUtilised)
            evaluatedCandidates += evalc

            if busUtilised is None: 
                solution.makeInfeasible()
                break
            
            busesUtilised.add(busUtilised)
            nBusesUtilised+=1

            solution.assignBus(busUtilised, s)

            driverUtilised, evalc = self.getBestDriver(s, problem)

            if driverUtilised is None:
                solution.makeInfeasible()
                break
            
            solution.assignDriver(driverUtilised, s)  

        solution.cost = self.calculateFinalCost(problem)          
        elapsedEvalTime = time.time() - elapsedEvalTime
        return(solution, elapsedEvalTime, evaluatedCandidates)

    def getBestBus(self, service, busesUtilised, problem, nBusesUtilised):
        maxCost = float('infinity')
        busUtilised = None
        cost = float('infinity')
        evaluatedCandidates = 0
        for i in range(0, problem.nBuses):
            b = problem.buses[i]
            if b.capacity < service.nPassengers:
                cost = float('infinity')
            elif b not in busesUtilised and nBusesUtilised >= problem.maxBuses:
                cost = float('infinity')
            elif len(b.services) != 0:
                for s_2 in b.services:
                    if s_2.startingTime + s_2.duration > service.startingTime:
                        cost = float('infinity')
                    else: 
                        cost = b.costMin * service.duration + b.costKm * service.distance
            else:
                cost = b.costMin * service.duration + b.costKm * service.distance

            if cost < maxCost:
                maxCost = cost
                busUtilised = b
            evaluatedCandidates+=1
        return (busUtilised, evaluatedCandidates)

    def getBestDriver(self, service, problem):
        maxCost = float('infinity')
        driverUtilised = None
        evaluatedCandidates = 0
        cost = float('infinity')
        for i in range(0, problem.nDrivers):
            d = problem.drivers[i]
            if d.timeWorked + service.duration > d.maxMinutes:
                cost = float('infinity')
            elif d.timeWorked + service.duration <= problem.BM:
                cost = problem.CBM * (d.timeWorked + service.duration)
            else:
                cost = problem.CBM * problem.BM + problem.CEM * (d.timeWorked + service.duration - problem.BM)
            if cost < maxCost:
                maxCost = cost
                driverUtilised = d
            evaluatedCandidates+=1
        return (driverUtilised, evaluatedCandidates)

    def calculateFinalCost(self, problem):
        cost = 0
        for b in problem.buses:
            for s in b.services:
                cost += b.costMin * s.duration + b.costKm * s.distance
        
        for d in problem.drivers:
            if d.timeWorked <= problem.BM:
                cost += d.timeWorked * problem.CBM
            else:
                cost += problem.CBM * problem.BM + (d.timeWorked - problem.BM) * problem.CEM
        return(cost)