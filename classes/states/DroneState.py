"""
base class for all other classes to inherit from
"""
class DroneState:
    def __init__(self):
        super().__init__()
        self.stateAsString = "DroneState -- BASE CLASS"

    def action(self, drone, eventList):
        pass

    def toString(self):
        return self.stateAsString

    def clean(self, drone):
        pass
