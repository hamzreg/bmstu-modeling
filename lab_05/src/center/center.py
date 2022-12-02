from center.operator import Operator
from center.computer import Computer
from center.client_generator import ClientGenerator
from center.event import Event, sort_events

class Center:
    def __init__(self, client_generator):
        self.client_generator = client_generator

    def service_clients(self):
        failures_number = 0

        self.client_generator.generate_client(0)
        generated_clients = 1
        events = [Event(self.client_generator, 
                  self.client_generator.time_next)]

        while generated_clients < self.client_generator.number:
            events = sort_events(events)
            event = events.pop(0)

            if isinstance(event.creator, ClientGenerator):
                operator = self.client_generator.choose_operator()

                if operator is None:
                    failures_number += 1
                else:
                    operator.set_busy()
                    operator.generate_time(event.time)
                    events.append(Event(operator, operator.time_next))

                self.client_generator.generate_client(event.time)
                generated_clients += 1
                events.append(Event(self.client_generator,
                              self.client_generator.time_next))
            elif isinstance(event.creator, Operator):
                operator = event.creator
                operator.set_free()

                computer = operator.get_computer()
                computer.append_request()

                if computer.is_free() and not computer.queue_empty():
                        computer.pop_request()
                        computer.set_busy()
                        computer.generate_time(event.time)
                        events.append(Event(computer, computer.time_next))
            elif isinstance(event.creator, Computer):
                computer = event.creator
                computer.set_free()

                if not computer.queue_empty():
                    computer.pop_request()
                    computer.set_busy()
                    computer.generate_time(event.time)
                    events.append(Event(computer, computer.time_next))

        return failures_number
