from objects.bus     import Bus 
from objects.driver  import Driver
from objects.service import Service

class Problem(object):
    def __init__(self, inputData):
        
        self.inputData = inputData
        
        nBuses = self.inputData.nBuses
        nDrivers = self.inputData.nDrivers
        nServices = self.inputData.nServices

        startingTimeService = self.inputData.startingTimeService
        durationTimeService = self.inputData.durationTimeService
        distanceService = self.inputData.distanceService
        nPassengersService = self.inputData.nPassengersService

        capacityBus = self.inputData.capacityBus
        costBusEurosMin = self.inputData.costBusEurosMin
        costBusEurosKm = self.inputData.costBusEurosKm

        maxMinutesDriver = self.inputData.maxMinutesDriver

        maxBuses = self.inputData.maxBuses
        BM = self.inputData.baseMinutes
        CBM = self.inputData.CBM
        CEM = self.inputData.CEM

        self.services = set()
        for sId in range(0, nServices):             
            st = startingTimeService[sId]
            t = durationTimeService[sId]
            d = distanceService[sId]
            nP = nPassengersService[sId]
            service = Service(sId, st, t, d, nP)
            self.services.add(service)            

        self.buses = set()
        for bId in range(0, nBuses):
            capacity = capacityBus[bId]
            costMin = costBusEurosMin[bId]
            costKm = costBusEurosKm[bId]
            bus = Bus(bId, capacity, costMin, costKm)
            self.buses.add(bus)

        self.drivers = set()
        for dId in range(0, nDrivers):
            maxM = maxMinutesDriver[dId]
            driver = Driver(dId, maxM)
            self.drivers.add(driver)

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
