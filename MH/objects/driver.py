class Driver(object):
    def __init__(self, driverId, maxMinutes):
        self.driverId = driverId
        self.timeWorked = 0       
        self.maxMinutes = maxMinutes
        self.services = set() #services that this driver is performing

    def addService(self, service):
        self.services.add(service)
