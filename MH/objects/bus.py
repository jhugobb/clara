class Bus(object):
    def __init__(self, busId, capacity, costMin, costKm):
        self.busId = busId
        self.capacity = capacity       
        self.costMin = costMin
        self.costKm = costKm
        self.services = set() #services that this bus is performing

    def addService(self, service):
        self.services.add(service)
