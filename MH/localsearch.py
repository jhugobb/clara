import copy, time

class LocalSearch(object):
    def __init__(self, config):
        self.enabledBuses = config.localSearchBuses
        self.enabledDrivers = config.localSearchDrivers
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.elapsedTime = 0
        self.iterations = 0

    def search(self, solution, solver, problem):
        if(not (self.enabledBuses or self.enabledDrivers)): return(solution)
        if(not solution.isFeasible()): return(solution)

        bestSolution = solution
        bestCost = solution.cost
        
        startEvalTime = time.time()
        iterations = 0
        
        # keep iterating while improvements are found
        keepIterating = True
        while(keepIterating):
            keepIterating = False
            iterations += 1
            
            neighbor = self.exploreNeighborhood(bestSolution, problem, solver)
            
            if neighbor is not None and (bestCost > neighbor.cost):
                bestSolution = neighbor
                bestCost = neighbor.cost
                keepIterating = True
        
        self.iterations += iterations
        self.elapsedTime += time.time() - startEvalTime
        
        return(bestSolution)
    
    def exploreNeighborhood(self, solution, problem, solver):
        buses = problem.buses
        drivers = problem.drivers
        if self.nhStrategy == 'Exchange':
            neighbor = None
            neighbor2 = None
            if self.enabledBuses:
                neighbor = self.exploreBuses(buses, solution, solver, problem)
            if self.enabledDrivers:
                if neighbor is not None:
                    neighbor2 = self.exploreDrivers(drivers, neighbor, solver, problem)
                else:
                   neighbor2 = self.exploreDrivers(drivers, solution, solver, problem)
            
            if neighbor is not None and neighbor2 is None:
                return neighbor
            else: return neighbor2
            

    def exploreBuses(self, buses, solution, solver, problem):
        bestcost = 0
        bestBus1 = None
        bestBus2 = None
        bestService1 = None
        bestService2 = None
        uncheckedBuses = list(buses)
        sortedBuses = self.getBusesByCurrCost(buses)
        for bus in sortedBuses:
            for service in bus.services:
                for bus2 in uncheckedBuses:
                    if bus.busId == bus2.busId: continue
                    service2, exchangeCost = self.tryChangeBus(bus, service, bus2)
                    if service2 is not None:            
                        if(self.policy == 'FirstImprovement'):
                            neighbor = copy.deepcopy(solution)
                            neighbor.createNeighborBus(bus, service, bus2, service2)
                            currCost = solver.calculateFinalCost(problem)
                            neighbor.cost = currCost
                            return(neighbor)
                        elif bestcost < exchangeCost:
                            bestBus1 = bus
                            bestBus2 = bus2
                            bestService1 = service
                            bestService2 = service2
                            bestcost = exchangeCost
                    service2 = None
                    exchangeCost = 0
            uncheckedBuses.remove(bus)
        if bestBus1 is not None:
            neighbor = copy.deepcopy(solution)
            neighbor.createNeighborBus(bestBus1, bestService1, bestBus2, bestService2)
            currCost = solver.calculateFinalCost(problem)
            neighbor.cost = currCost
            return(neighbor)
        else: return None

    def exploreDrivers(self, drivers, solution, solver, problem):
        bestcost = 0
        bestDriver1 = None
        bestDriver2 = None
        bestService1 = None
        bestService2 = None
        sortedDrivers = self.getDriversByCurrCost(drivers, problem)
        for driver in sortedDrivers:
            for service in driver.services:
                for driver2 in drivers:
                    if driver.driverId == driver2.driverId: continue
                    service2, exchangeCost = self.tryChangeDriver(driver, service, driver2, problem)
                    if service2 is not None:            
                        if(self.policy == 'FirstImprovement'):
                            neighbor = copy.deepcopy(solution)
                            neighbor.createNeighborDriver(driver, service, driver2, service2)
                            currCost = solver.calculateFinalCost(problem)
                            neighbor.cost = currCost
                            return(neighbor)
                        elif bestcost < exchangeCost:
                            bestDriver1 = driver
                            bestDriver2 = driver2
                            bestService1 = service
                            bestService2 = service2
                            bestcost = exchangeCost
                    service2 = None
                    exchangeCost = 0
        if bestDriver1 is not None:
            neighbor = copy.deepcopy(solution)
            neighbor.createNeighborDriver(bestDriver1, bestService1, bestDriver2, bestService2)
            currCost = solver.calculateFinalCost(problem)
            neighbor.cost = currCost
            return(neighbor)
        else: return None

    def getBusesByCurrCost(self, buses):
        return sorted(buses, key = lambda bus: sum(map(lambda service: bus.costMin*service.duration+bus.costKm*service.distance, bus.services)), reverse=True)
    
    def getDriversByCurrCost(self, drivers, problem):
        for driver in drivers:
            driver.cost = 0
            if driver.timeWorked <= problem.BM:
                driver.cost += driver.timeWorked * problem.CBM
            else:
                driver.cost += problem.CBM * problem.BM + (driver.timeWorked - problem.BM) * problem.CEM
        return sorted(drivers, key = lambda driver: driver.cost, reverse = True)
        #return sorted(buses, key = lambda bus: sum(map(lambda service: bus.costMin*service.duration+bus.costKm*service.distance, bus.services)), reverse=True)


    def tryChangeBus(self, bus, service, bus2):
        bestService = None
        cost = None
        bestCost = sum(map(lambda ser: bus.costMin*ser.duration+bus.costKm*ser.distance, bus.services))
        bestCost += sum(map(lambda ser: bus2.costMin*ser.duration+bus2.costKm*ser.distance, bus2.services))
        initialCost = bestCost
        for s in bus2.services:
            isCompatible = True
            for s2 in bus.services:
                    if s2.serviceId == service.serviceId: continue
                    if s2.startingTime < s.startingTime:
                        if s2.startingTime + s2.duration > s.startingTime:
                            isCompatible = False
                            break
                    elif s.startingTime + s.duration > s2.startingTime:
                        isCompatible = False
                        break
            for s2 in bus2.services:
                    if s2.serviceId == s.serviceId: continue
                    if s2.startingTime < service.startingTime:
                        if s2.startingTime + s2.duration > service.startingTime:
                            isCompatible = False
                            break
                    elif service.startingTime + service.duration > s2.startingTime:
                        isCompatible = False
                        break
            if isCompatible:
                bus.services.remove(service)
                bus2.services.remove(s)
                bus.services.add(s)
                bus2.services.add(service)
                cost  = sum(map(lambda ser: bus.costMin*ser.duration+bus.costKm*ser.distance, bus.services))
                cost += sum(map(lambda ser: bus2.costMin*ser.duration+bus2.costKm*ser.distance, bus2.services))
                if cost < bestCost:
                    bestService = s
                    bestCost = cost
                
                bus2.services.remove(service)
                bus.services.remove(s)
                bus2.services.add(s)
                bus.services.add(service)
        return bestService, initialCost - bestCost

    def tryChangeDriver(self, driver, service, driver2, problem):
        bestService = None
        cost = None
        if driver.timeWorked <= problem.BM:
            bestCost =  driver.timeWorked * problem.CBM  
        else: 
            bestCost = problem.CBM * problem.BM + (driver.timeWorked - problem.BM) * problem.CEM
        if driver2.timeWorked <= problem.BM:
            bestCost += driver2.timeWorked * problem.CBM 
        else:
            bestCost += problem.CBM * problem.BM + (driver2.timeWorked - problem.BM) * problem.CEM
        initialCost = bestCost
        for s in driver2.services:
            isCompatible = True
            for s2 in driver.services:
                    if s2.serviceId == service.serviceId: continue
                    if s2.startingTime < s.startingTime:
                        if s2.startingTime + s2.duration > s.startingTime:
                            isCompatible = False
                            break
                    elif s.startingTime + s.duration > s2.startingTime:
                        isCompatible = False
                        break
            for s2 in driver2.services:
                    if s2.serviceId == s.serviceId: continue
                    if s2.startingTime < service.startingTime:
                        if s2.startingTime + s2.duration > service.startingTime:
                            isCompatible = False
                            break
                    elif service.startingTime + service.duration > s2.startingTime:
                        isCompatible = False
                        break
            if isCompatible:
                driver.services.remove(service)
                driver.timeWorked -= service.duration
                driver2.services.remove(s)
                driver2.timeWorked -= s.duration
                driver.services.add(s)
                driver.timeWorked += s.duration
                driver2.services.add(service)
                driver2.timeWorked += service.duration
                
                cost = driver.timeWorked * problem.CBM if driver.timeWorked <= problem.BM else problem.CBM * problem.BM + (driver.timeWorked - problem.BM) * problem.CEM
                cost += driver2.timeWorked * problem.CBM if driver2.timeWorked <= problem.BM else problem.CBM * problem.BM + (driver2.timeWorked - problem.BM) * problem.CEM
                if cost < bestCost:
                    bestService = s
                    bestCost = cost
                
                driver2.services.remove(service)
                driver2.timeWorked -= service.duration
                driver.services.remove(s)
                driver.timeWorked -= s.duration
                driver2.services.add(s)
                driver2.timeWorked += s.duration
                driver.services.add(service)
                driver.timeWorked += service.duration
        return bestService, initialCost - bestCost

    def printPerformance(self):
        if(not (self.enabledBuses or self.enabledDrivers)): return
        
        avg_evalTimePerIteration = 0.0
        if(self.iterations != 0):
            avg_evalTimePerIteration = 1000.0 * self.elapsedTime / float(self.iterations)
        
        print ('')
        print ('Local Search Performance:')
        print ('  Num. Iterations Eval.', self.iterations)
        print ('  Total Eval. Time     ', self.elapsedTime, 's')
        print ('  Avg. Time / Iteration', avg_evalTimePerIteration, 'ms')
