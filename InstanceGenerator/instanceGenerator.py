import os, random

# Generate instances based on read configuration. 
class instanceGenerator(object):
    def __init__(self, config):
        self.config = config
    
    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        nServices = self.config.nServices
        nBuses = self.config.nBuses
        nDrivers = self.config.nDrivers  
        
        minStartingTimeService = self.config.minStartingTimeService
        maxStartingTimeService = self.config.maxStartingTimeService
        minDurationTimeService = self.config.minDurationTimeService
        maxDurationTimeService = self.config.maxDurationTimeService
        minDistanceService = self.config.minDistanceService
        maxDistanceService = self.config.maxDistanceService
        minNPassengersService = self.config.minNPassengersService
        maxNPassengersService = self.config.maxNPassengersService

        minCapacityBus = self.config.minCapacityBus
        maxCapacityBus = self.config.maxCapacityBus
        minCostBusEurosMin = self.config.minCostBusEurosMin
        maxCostBusEurosMin = self.config.maxCostBusEurosMin
        minCostBusEurosKm = self.config.minCostBusEurosKm
        maxCostBusEurosKm = self.config.maxCostBusEurosKm

        minMaxMinutesDriver = self.config.minMaxMinutesDriver
        maxMaxMinutesDriver = self.config.maxMaxMinutesDriver

        maxBuses = self.config.maxBuses
        CBM = self.config.CBM
        CEM = self.config.CEM
        BM = self.config.BM


        if(not os.path.isdir(instancesDirectory)):
            raise Exception('Directory(%s) does not exist' % instancesDirectory)

        for i in range(0, numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            st_s = [] #starting time of each service
            duration_s = [] # duration " " "
            distance_s = [] # distance " " "
            nPassengers_s = [] # number of passengers " " "
            for s in range(0, nServices):
                startingTimeService = random.randint(minStartingTimeService, maxStartingTimeService)
                durationTimeService = random.randint(minDurationTimeService, maxDurationTimeService)
                distanceService     = round(random.uniform(minDistanceService, maxDistanceService), 2)
                nPassengersService  = random.randint(minNPassengersService, maxNPassengersService)
                st_s.append(startingTimeService)
                duration_s.append(durationTimeService)
                distance_s.append(distanceService)
                nPassengers_s.append(nPassengersService)
            
            capacity_b = []
            costMin_b = []
            costKm_b = []
            for b in range(0, nBuses):
                capacityBus = random.randint(minCapacityBus, maxCapacityBus)
                costMinBus  = round(random.uniform(minCostBusEurosMin, maxCostBusEurosMin), 2)
                costKmBus   = round(random.uniform(minCostBusEurosKm, maxCostBusEurosKm), 2)
                capacity_b.append(capacityBus)
                costMin_b.append(costMinBus)
                costKm_b.append(costKmBus)
            
            maxMin_d = []
            for d in range(0, nDrivers):
                maxMinDriver = random.randint(minMaxMinutesDriver, maxMaxMinutesDriver)
                maxMin_d.append(maxMinDriver)

            fInstance.write('nServices=%d;\n' % nServices)
            fInstance.write('nBuses=%d;\n' % nBuses)
            fInstance.write('nDrivers=%d;\n' % nDrivers)

            fInstance.write('\n')
            
            # translate vector of floats into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('startingTimeService=[%s];\n' % (' '.join(map(str, st_s))))
            fInstance.write('durationTimeService=[%s];\n' % (' '.join(map(str, duration_s))))
            fInstance.write('distanceService=[%s];\n' % (' '.join(map(str, distance_s))))
            fInstance.write('nPassengersService=[%s];\n' % (' '.join(map(str, nPassengers_s))))

            fInstance.write('\n')

            fInstance.write('capacityBus=[%s];\n' % (' '.join(map(str, capacity_b))))
            fInstance.write('costBusEurosMin=[%s];\n' % (' '.join(map(str, costMin_b))))
            fInstance.write('costBusEurosKm=[%s];\n' % (' '.join(map(str, costKm_b))))
            
            fInstance.write('\n')

            fInstance.write('maxMinutesDriver=[%s];\n' % (' '.join(map(str, maxMin_d))))

            fInstance.write('\n')
            
            fInstance.write('maxBuses=%s;\n' % maxBuses)
            fInstance.write('baseMinutes=%s;\n' % BM)
            fInstance.write('CBM=%s;\n' % CBM)
            fInstance.write('CEM=%s;\n' % CEM)

            fInstance.close()
