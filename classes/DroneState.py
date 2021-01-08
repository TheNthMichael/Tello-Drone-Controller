class States:
        WAITING = 0
        USER_CONTROL = 1
        SEARCHING = 2
        TRACKING = 3
        EXIT = 4


"""
Format:
State -> Transition : StateChange : lambda defining the transition
State -> Action : lambda defining the action

Planned States:
    different forms of SEARCHING and TRACKING
    selecting tracking bounding box and TRACKING
tracking modes:
"""
class StateMachine:
    def __init__(self):
        # drone should initially be waiting
        self.state = States.WAITING
        self.auto = False
        self.state_transition = {
            States.WAITING : {
                States.USER_CONTROL : prepare_user_control,
                States.SEARCHING : prepare_searching,
                States.EXIT : prepare_exit
            },
            States.USER_CONTROL : {
                States.SEARCHING : prepare_searching,
                States.WAITING : pause,
                States.EXIT : prepare_exit
            },
            States.SEARCHING : {
                States.TRACKING : prepare_tracking,
                States.USER_CONTROL : prepare_user_control,
                States.EXIT : prepare_exit
            },
            States.TRACKING : {
                States.SEARCHING : prepare_searching,
                States.USER_CONTROL : prepare_user_control,
                States.EXIT : prepare_exit
            }
        }
        self.state_machine = {
            States.WAITING : action_waiting,
            States.USER_CONTROL : action_user_control,
            States.SEARCHING : action_searching,
            States.TRACKING : action_tracking,
            States.EXIT : action_exit
        }
    
    def state_change(self, input):
        state_changes = self.state_transition[self.state]
        self.state = state_changes[input]
        if self.state == States.SEARCHING or self.state == States.TRACKING:
            self.auto = True
        else:
            self.auto = False
    
    def state_action(self):
        self.state_action[self.state]()
    
