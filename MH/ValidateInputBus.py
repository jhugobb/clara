'''
AMMM Assignement Heuristics vBeta
Instance File Validator for the Project.
Copyright 2018 Hugo Ballesteros & Ivan Salfati.

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
# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.

class ValidateInputBus(object):
	@staticmethod
	def validate(data):
		#Validate that all input parameters was found
		for paramName in ['nServices', 'nBuses', 'nDrivers', 'startingTimeService', 'durationTimeService', 'distanceService', 'nPassengersService', 'capacityBus', 'costBusEurosMin', 'costBusEurosKm', 'maxMinutesDriver', 'maxBuses', 'baseMinutes', 'CBM', 'CEM']:
			if(not data.__dict__.has_key(paramName)):
				raise Exception('Parameter/Set(%s) not contained in Input Data' % str(paramName))

		#Validate nServices
		nServices = data.nServices
		if(not isinstance(nServices, int) or nServices <= 0):
			raise Exception('nServices(%s) has to be a positive integer value.' % str(nServices))
		
		#Validate nBuses
		nBuses = data.nBuses
		if(not isinstance(nBuses, int) or nBuses <= 0):
			raise Exception('nBuses(%s) has to be a positive integer value.' % str(nBuses))
		
		#Validate nDrivers
		nDrivers = data.nDrivers
		if(not isinstance(nDrivers, int) or nDrivers <= 0):
			raise Exception('nDrivers(%s) has to be a positive integer value.' % str(nDrivers))
		
		#Validate startingTimeService
		startingTimeService = data.startingTimeService
		if(len(startingTimeService) != nServices):
			raise Exception('Size of startingTimeService(%d) does not match with the value of nServices(%d).' % (len(startingTimeService), nServices))
		
		for value in startingTimeService:
			if(not isinstance(value, int) or value <= 0):
				raise Exception('Invalid parameter value(%s) in startingTimeService. Should be an integer greater or equal than zero.' % str(value))
		
		#Validate durationTimeService+
		durationTimeService = data.durationTimeService
		if(len(durationTimeService) != nServices):
			raise Exception('Size of durationTimeService(%d) does not match with the value of nServices(%d).' % (len(durationTimeService), nServices))
		
		for value in durationTimeService:
			if(not isinstance(value, int) or value <= 0):
				raise Exception('Invalid parameter value(%s) in durationTimeService. Should be an integer greater or equal than zero.' % str(value))
					
		#Validate distanceService
		distanceService = data.distanceService
		if(len(distanceService) != nServices):
			raise Exception('Size of distanceService(%d) does not match with the value of nServices(%d).' % (len(distanceService), nServices))
			
		for value in distanceService:
			if(not isinstance(value, (int, float)) or (value <= 0)):
				raise Exception('Invalid parameter value(%s) in distanceService. Should be an integer or floar greater or equal than zero.' % str(value))
		
		#Validate nPassengersService
		nPassengersService = data.nPassengersService
		if(len(nPassengersService) != nServices):
			raise Exception('Size of nPassengersService(%d) does not match with the value of nServices(%d).' % (len(nPassengersService), nServices))
		
		for value in nPassengersService:
			if(not isinstance(value, int) or value < 1):
				raise Exception('Invalid parameter value(%s) in nPassengersService. Should be an integer greater or equal than one.' % str(value))
		
		#Validate capacityBus
		capacityBus = data.capacityBus
		if(len(capacityBus) != nBuses):
			raise Exception('Size of capacityBus(%d) does not match with the value of nBuses(%d).' % (len(capacityBus), nBuses))
			
		for value in capacityBus:
			if(not isinstance(value, int) or value < 1):
				raise Exception('Invalid parameter value(%s) in capacityBus. Should be an integer greater or equal than one.' % str(value))
		
		#Validate costBusEurosMin
		costBusEurosMin = data.costBusEurosMin
		if(len(costBusEurosMin) != nBuses):
			raise Exception('Size of costBusEurosMin(%d) does not match with the value of nBuses(%d).' % (len(costBusEurosMin), nBuses))
			
		for value in costBusEurosMin:
			if(not isinstance(value, (int, float)) or (value < 0)):
				raise Exception('Invalid parameter value(%s) in costBusEurosMin. Should be an integer or float greater than zero.' % str(value))
				
		#Validate costBusEurosKm
		costBusEurosKm = data.costBusEurosKm
		if(len(costBusEurosKm) != nBuses):
			raise Exception('Size of costBusEurosKm(%d) does not match with the value of nBuses(%d).' % (len(costBusEurosKm), nBuses))
			
		for value in costBusEurosKm:
			if(not isinstance(value, (int, float)) or value < 0):
				raise Exception('Invalid parameter value(%s) in costBusEurosKm. Should be an integer or float greater than zero.' % str(value))
		
		#Validate maxMinutesDriver
		maxMinutesDriver = data.maxMinutesDriver
		if(len(maxMinutesDriver) != nDrivers):
			raise Exception('Size of maxMinutesDriver(%d) does not match with the value of nDrivers(%d).' % (len(maxMinutesDriver), nDrivers))
		
		for value in maxMinutesDriver:
			if(not isinstance(value, int) or value < 1):
				raise Exception('Invalid parameter value(%s) in maxMinutesDriver. Should be an integer greater than one.' % str(value))
		
		#Validate maxBuses
		maxBuses = data.maxBuses
		if(not isinstance(maxBuses, int) or maxBuses <= 0):
			raise Exception('maxBuses(%s) has to be a positive integer value.' % str(maxBuses))
		
		#Validate baseMinutes
		baseMinutes = data.baseMinutes
		if(not isinstance(baseMinutes, int) or baseMinutes <= 0):
			raise Exception('baseMinutes(%s) has to be a positive integer value.' % str(baseMinutes))
		
		#Validate CBM
		CBM = data.CBM
		if(not isinstance(CBM, int) or CBM <= 0):
			raise Exception('CBM(%s) has to be a positive integer value.' % str(CBM))
		
		#Validate CEM
		CEM = data.CEM
		if(not isinstance(CEM, int) or CEM <= 0):
			raise Exception('CEM(%s) has to be a positive integer value.' % str(CEM))
				
				