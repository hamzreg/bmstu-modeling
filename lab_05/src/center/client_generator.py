from center.time_generator import TimeGenerator


class ClientGenerator:
    def __init__(self, time_value, time_limit, operators, number):
        self.time_generator = TimeGenerator(time_value - time_limit,
                                            time_value + time_limit)
        self.operators = self.__sort_operators(operators)
        self.time_next = 0
        self.number = number

    def generate_client(self, time_prev):
        self.time_next = time_prev + \
            self.time_generator.get_time_interval()

    def choose_operator(self):
        for operator in self.operators:
            if operator.is_free():
                return operator

        return None

    def __sort_operators(self, operators):
        return sorted(operators, key= lambda operator: operator.max_time)
