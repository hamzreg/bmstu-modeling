class Receiver:
    def __init__(self, time_value, time_limit):
        self.time_generator = 
             TimeGenerator(time_value - time_limit,
                           time_value + time_limit)
        self.queue = []
        self.time_next = 0
        self.free = True

    def generate_time(self, prev_time):
        self.time_next = prev_time + \
        self.time_generator.get_time_interval()

    def is_free(self):
        return self.free

    def set_free(self):
        self.free = True

    def set_busy(self):
        self.free = False

    def queue_empty(self):
        if self.queue:
            return False
        return True

    def append_enrollee(self, department_type):
        self.queue.append(department_type)

    def pop_enrollee(self):
        return self.queue.pop(0)
