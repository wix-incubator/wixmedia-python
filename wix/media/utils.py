import time


class BackOff(object):
    def __init__(self, initial_interval_wait_time=5, max_interval_wait_time=20, max_wait_time=60):
        self.initial_interval_wait_time = initial_interval_wait_time
        self.max_interval_wait_time     = max_interval_wait_time
        self.wait_time                  = initial_interval_wait_time
        self.max_wait_time              = max_wait_time if initial_interval_wait_time <= max_wait_time else initial_interval_wait_time
        self.total_waited               = 0

    def reset(self):
        self.wait_time    = self.initial_interval_wait_time
        self.total_waited = 0

    def wait(self):
        if self.total_waited >= self.max_wait_time:
            return False

        time.sleep(self.wait_time)
        self.total_waited += self.wait_time

        if self.wait_time < self.max_interval_wait_time:
            self.wait_time = min(self.wait_time * 2, self.max_interval_wait_time)

        self.wait_time = min(self.wait_time, max(self.max_wait_time - self.total_waited, 0))

        return self.wait_time > 0
