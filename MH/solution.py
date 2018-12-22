import copy, time
from problem import Problem

# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(Problem):
    @staticmethod
    def createEmptySolution(config, problem):
        solution = Solution(problem.inputData)
        solution.setVerbose(config.verbose)
        return(solution)

    def __init__(self, inputData):
        super(Solution, self).__init__(inputData)
        
        self.serviceIdtoBus = {}             # hash table: service Id => bus Id
        self.serviceIdtoDriver = {}          # hash table: service Id => driver Id
        
        self.cost = 0.0
        
        self.feasible = True
        self.verbose = False
    
    def setVerbose(self, verbose):
        if(not isinstance(verbose, (bool)) or (verbose not in [True, False])):
            raise Exception('verbose(%s) has to be a boolean value.' % str(verbose))
        self.verbose = verbose
    
    def makeInfeasible(self):
        self.feasible = False
        self.cost = float('infinity')
    
    def isFeasible(self):
        return(self.feasible)

    def assignBus(self, bus, service):
        self.serviceIdtoBus[service.serviceId] = bus.busId
        bus.services.add(service)
        service.bus = bus
    
    def assignDriver(self, driver, service):
        self.serviceIdtoDriver[service.serviceId] = driver.driverId
        driver.services.add(service)
        driver.timeWorked += service.duration
        service.driver = driver

    def createNeighborBus(self, bus, service, bus2, service2):
        bus.services.remove(service)
        bus2.services.remove(service2)
        bus.services.add(service2)
        bus2.services.add(service)

        self.serviceIdtoBus.pop(service.serviceId, None)
        self.serviceIdtoBus[service.serviceId] = bus2.busId
        self.serviceIdtoBus.pop(service2.serviceId, None)
        self.serviceIdtoBus[service2.serviceId] = bus.busId

    def createNeighborDriver(self, driver, service, driver2, service2):
        driver.services.remove(service)
        driver.timeWorked -= service.duration
        driver2.services.remove(service2)
        driver2.timeWorked -= service2.duration
        driver.services.add(service2)
        driver.timeWorked += service2.duration
        driver2.services.add(service)
        driver2.timeWorked += service.duration

        self.serviceIdtoDriver.pop(service.serviceId, None)
        self.serviceIdtoDriver[service.serviceId] = driver2.driverId
        self.serviceIdtoDriver.pop(service2.serviceId, None)
        self.serviceIdtoDriver[service2.serviceId] = driver.driverId
        

    
    def __str__(self):  # toString equivalent
        nServices = self.inputData.nServices
        nBuses = self.inputData.nBuses
        nDrivers = self.inputData.nDrivers
        
        strSolution = 'z = %10.8f;\n' % self.cost
        
        # Xhk: decision variable containing the assignment of threads to cores
        # pre-fill with no assignments (all-zeros)
        xbs = []
        for b in range(0, nBuses):         # h = 0..(nThreads-1)
            xbsEntry = [0] * nServices     # results in a vector of 0's with nCores elements
            xbs.append(xbsEntry)

        xds = []
        for d in range(0, nDrivers):
            xdsEntry = [0] * nServices
            xds.append(xdsEntry)

        for serviceId, busId in self.serviceIdtoBus.items():
            xbs[busId][serviceId] = 1

        for serviceId, driverId in self.serviceIdtoDriver.items():
            xds[driverId][serviceId] = 1
        
        strSolution += 'xbs = [\n'
        for xbsEntry in xbs:
            strSolution += '\t[ '
            for xbsValue in xbsEntry:
                strSolution += str(xbsValue) + ' '
            strSolution += ']\n'
        strSolution += '];\n'

        strSolution += 'xds = [\n'
        for xdsEntry in xds:
            strSolution += '\t[ '
            for xdsValue in xdsEntry:
                strSolution += str(xdsValue) + ' '
            strSolution += ']\n'
        strSolution += '];\n'

        return(strSolution)

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
