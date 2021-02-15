"""
base class for all other classes to inherit from
"""
class DroneState:
    def __init__(self):
        super().__init__()
        self.state_type = States.EXIT
        self.state_transition = {
                States.EXIT : lambda : Exit()
            }

    def action(self, drone, eventList):
        pass

    def change(self, state=States.EXIT):
        transition = self.state_transition[state]
        return transition()

    def clean(self, drone):
        pass
