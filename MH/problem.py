from objects.bus     import Bus 
from objects.driver  import Driver
from objects.service import Service

class Problem(object):
    def __init__(self, inputData):
        
        self.inputData = inputData
        
        self.nBuses = self.inputData.nBuses
        self.nDrivers = self.inputData.nDrivers
        self.nServices = self.inputData.nServices

        self.startingTimeService = self.inputData.startingTimeService
        self.durationTimeService = self.inputData.durationTimeService
        self.distanceService = self.inputData.distanceService
        self.nPassengersService = self.inputData.nPassengersService

        self.capacityBus = self.inputData.capacityBus
        self.costBusEurosMin = self.inputData.costBusEurosMin
        self.costBusEurosKm = self.inputData.costBusEurosKm

        self.maxMinutesDriver = self.inputData.maxMinutesDriver

        self.maxBuses = self.inputData.maxBuses
        self.BM = self.inputData.baseMinutes
        self.CBM = self.inputData.CBM
        self.CEM = self.inputData.CEM
        self.services = list()
        for sId in range(0, self.nServices):     
            st = self.startingTimeService[sId]
            t = self.durationTimeService[sId]
            d = self.distanceService[sId]
            nP = self.nPassengersService[sId]
            service = Service(sId, st, t, d, nP)
            self.services.append(service)            

        self.buses = list()
        for bId in range(0, self.nBuses):
            capacity = self.capacityBus[bId]
            costMin = self.costBusEurosMin[bId]
            costKm = self.costBusEurosKm[bId]
            bus = Bus(bId, capacity, costMin, costKm)
            self.buses.append(bus)

        self.drivers = list()
        for dId in range(0, self.nDrivers):
            maxM = self.maxMinutesDriver[dId]
            driver = Driver(dId, maxM)
            self.drivers.append(driver)

    def checkInstance(self):
        # check max capacity of a bus 
        # check time of a driver vs max time of services
        maxBusCapacity = 0
        for bus in self.buses:
            if bus.capacity > maxBusCapacity:
                maxBusCapacity = bus.capacity
        maxNPassengers = 0
        maxMinutes = 0
        for service in self.services:
            if service.duration > maxMinutes:
                maxMinutes = service.duration
            if service.nPassengers > maxNPassengers:
                maxNPassengers = service.nPassengers
        
        maxDriverTime = 0
        for driver in self.drivers:
            if driver.maxMinutes > maxDriverTime:
                maxDriverTime = driver.maxMinutes
        
        if maxBusCapacity < maxNPassengers: return(False)
        if maxDriverTime < maxMinutes: return(False)

        return(True)
