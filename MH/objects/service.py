class Service(object):
    def __init__(self, serviceId, startingTime, duration, distance, nPassengers):
        self.serviceId = serviceId
        self.startingTime = startingTime
        self.duration = duration
        self.distance = distance
        self.nPassengers = nPassengers
        self.bus = None
        self.driver = None