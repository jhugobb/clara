'''
AMMM Instance Generator v1.0
Config attributes validator.
Copyright 2016 Luis Velasco and Lluis Gifre.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# Validate config attributes read from a DAT file. 
class validateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                          'nServices', 'nBuses', 'nDrivers', 'minStartingTimeService', 'maxStartingTimeService',
                          'minDurationTimeService', 'maxDurationTimeService', 'minDistanceService',
                          'maxDistanceService', 'minNPassengersService', 'maxNPassengersService',
                          'minCapacityBus', 'maxCapacityBus', 'minCostBusEurosMin', 'maxCostBusEurosMin',
                          'minCostBusEurosKm', 'maxCostBusEurosKm', 'minMaxMinutesDriver', 'maxMaxMinutesDriver',
                          'maxBuses', 'CBM', 'CEM', 'BM']:
            if(not paramName in  data.__dict__):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))
        
        instancesDirectory = data.instancesDirectory
        if(len(instancesDirectory) == 0): raise Exception('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if(len(fileNamePrefix) == 0): raise Exception('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if(len(fileNameExtension) == 0): raise Exception('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if(not isinstance(numInstances, (int)) or (numInstances <= 0)):
            raise Exception('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        nServices = data.nServices
        if(not isinstance(nServices, (int)) or (nServices <= 0)):
            raise Exception('nServices(%s) has to be a positive integer value.' % str(nServices))
        
        nBuses = data.nBuses
        if(not isinstance(nBuses, (int)) or (nBuses <= 0)):
            raise Exception('nBuses(%s) has to be a positive integer value.' % str(nBuses))
        
        nDrivers = data.nDrivers
        if(not isinstance(nDrivers, (int)) or (nDrivers <= 0)):
            raise Exception('nDrivers(%s) has to be a positive integer value.' % str(nDrivers))

        minStartingTimeService = data.minStartingTimeService
        if(not isinstance(minStartingTimeService, (int)) or (minStartingTimeService <= 0)):
            raise Exception('minStartingTimeService(%s) has to be a positive integer value.' % str(minStartingTimeService))

        maxStartingTimeService = data.maxStartingTimeService
        if(not isinstance(maxStartingTimeService, (int)) or (maxStartingTimeService <= 0)):
            raise Exception('maxStartingTimeService(%s) has to be a positive integer value.' % str(maxStartingTimeService))

        minDistanceService = data.minDistanceService
        if(not isinstance(minDistanceService, (int)) or (minDistanceService <= 0)):
            raise Exception('minDistanceService(%s) has to be a positive integer value.' % str(minDistanceService))

        maxDistanceService = data.maxDistanceService
        if(not isinstance(maxDistanceService, (int)) or (maxDistanceService <= 0)):
            raise Exception('maxDistanceService(%s) has to be a positive integer value.' % str(maxDistanceService))

        minNPassengersService = data.minNPassengersService
        if(not isinstance(minNPassengersService, (int)) or (minNPassengersService <= 0)):
            raise Exception('minNPassengersService(%s) has to be a positive integer value.' % str(minNPassengersService))
        
        maxNPassengersService = data.maxNPassengersService
        if(not isinstance(maxNPassengersService, (int)) or (maxNPassengersService <= 0)):
            raise Exception('maxNPassengersService(%s) has to be a positive integer value.' % str(maxNPassengersService))

        minCapacityBus = data.minCapacityBus
        if(not isinstance(minCapacityBus, (int)) or (minCapacityBus <= 0)):
            raise Exception('minCapacityBus(%s) has to be a positive integer value.' % str(minCapacityBus))

        maxCapacityBus = data.maxCapacityBus
        if(not isinstance(maxCapacityBus, (int)) or (maxCapacityBus <= 0)):
            raise Exception('maxCapacityBus(%s) has to be a positive integer value.' % str(maxCapacityBus))

        minCostBusEurosMin = data.minCostBusEurosMin
        if(not isinstance(minCostBusEurosMin, (int, float)) or (minCostBusEurosMin <= 0)):
            raise Exception('minCostBusEurosMin(%s) has to be a positive float value.' % str(minCostBusEurosMin))

        maxCostBusEurosMin = data.maxCostBusEurosMin
        if(not isinstance(maxCostBusEurosMin, (int, float)) or (maxCostBusEurosMin <= 0)):
            raise Exception('maxCostBusEurosMin(%s) has to be a positive float value.' % str(maxCostBusEurosMin))
        
        minCostBusEurosKm = data.minCostBusEurosKm
        if(not isinstance(minCostBusEurosKm, (int, float)) or (minCostBusEurosKm <= 0)):
            raise Exception('minCostBusEurosKm(%s) has to be a positive float value.' % str(minCostBusEurosKm))
        
        maxCostBusEurosKm = data.maxCostBusEurosKm
        if(not isinstance(maxCostBusEurosKm, (int, float)) or (maxCostBusEurosKm <= 0)):
            raise Exception('maxCostBusEurosKm(%s) has to be a positive float value.' % str(maxCostBusEurosKm))

        minMaxMinutesDriver = data.minMaxMinutesDriver
        if(not isinstance(minMaxMinutesDriver, (int)) or (minMaxMinutesDriver <= 0)):
            raise Exception('minMaxMinutesDriver(%s) has to be a positive integer value.' % str(minMaxMinutesDriver))
        
        maxMaxMinutesDriver = data.maxMaxMinutesDriver
        if(not isinstance(maxMaxMinutesDriver, (int)) or (maxMaxMinutesDriver <= 0)):
            raise Exception('maxMaxMinutesDriver(%s) has to be a positive integer value.' % str(maxMaxMinutesDriver))
        
        maxBuses = data.maxBuses
        if(not isinstance(maxBuses, (int)) or (maxBuses <= 0)):
            raise Exception('maxBuses(%s) has to be a positive integer value.' % str(maxBuses))
        
        CBM = data.CBM
        if(not isinstance(CBM, (int)) or (CBM <= 0)):
            raise Exception('CBM(%s) has to be a positive integer value.' % str(CBM))
        
        CEM = data.CEM
        if(not isinstance(CEM, (int)) or (CEM <= 0)):
            raise Exception('CEM(%s) has to be a positive integer value.' % str(CEM))
        
        BM = data.BM
        if(not isinstance(BM, (int)) or (BM <= 0)):
            raise Exception('BM(%s) has to be a positive integer value.' % str(BM))
