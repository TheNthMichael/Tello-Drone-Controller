class Pid:
    def __init__(self, kp, ki, kd, dt,):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.sum_error = 0
        self.last_error = 0
    
    def output(self, error):
        p = self.kp * error
        self.sum_error += error
        i = self.ki * self.sum_error * self.dt
        d = self.kp * (error - self.last_error) * (1.0 / self.dt)
        self.last_error = error
        return p + i + d