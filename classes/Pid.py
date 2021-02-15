class Pid:
    def __init__(self, kp, ki, kd, dt, clamp_lower, clamp_higher):
        assert(clamp_lower < clamp_higher)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.clamp_lower = clamp_lower
        self.clamp_higher = clamp_higher
        self.sum_error = 0
        self.last_error = 0

    def reset(self):
        self.sum_error = 0
        self.last_error = 0

    def clamp(self, x):
        if x > self.clamp_higher:
            return self.clamp_higher
        elif x < self.clamp_lower:
            return self.clamp_lower
        return x

    
    def output(self, error):
        p = self.kp * error
        self.sum_error += error
        i = self.ki * self.sum_error * self.dt
        d = self.kp * (error - self.last_error) * (1.0 / self.dt)
        self.last_error = error
        return self.clamp(p + i + d)