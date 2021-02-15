import unittest
import sys
sys.path.append('../classes')
import DroneState

class TestDroneState(unittest.TestCase):
    """
    Test that all states can be created without throwing an exception
    """
    def createAllStates(self):
        noException = True
        try:
            stateObjectList = [
                DroneState.Waiting(),
                DroneState.UserControl(),
                DroneState.UserControlPlusTest(),
                DroneState.AutoFaceFocus(),
                DroneState.Exit()
            ]
        except Exception:
            noException = False
        self.assertTrue(noException)


if __name__ == '__main__':
    unittest.main()