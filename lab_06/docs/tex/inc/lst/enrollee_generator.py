class EnrolleeGenerator:
    def __init__(self, time_value, time_limit, handlers, number):
        self.time_generator = 
             TimeGenerator(time_value - time_limit,
                           time_value + time_limit)
        self.handlers = self.__sort_handlers(handlers)
        self.time_next = 0
        self.number = number

    def generate_enrollee(self, time_prev):
        self.time_next = time_prev + \
            self.time_generator.get_time_interval()

    def choose_handler(self):
        for handler in self.handlers:
            if handler.is_free():
                return handler

        return None

    def __sort_handlers(self, handlers):
        return sorted(handlers, key= lambda handler: handler.max_time)

def choose_department_type(probabilities):
    num = random()
    value = 0

    for type, probability in enumerate(probabilities):
        value += probability

        if value > num:
            return type
