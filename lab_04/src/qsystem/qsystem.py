from random import random
from dataclasses import dataclass

from qsystem.generator import Generator
from qsystem.handler import Handler


@dataclass
class State:
    generation = 0
    handling = 1

@dataclass
class Constants:
    time = 0
    state = 1


class QSystem:
    def __init__(self, a, b, mu, sigma, msg_number, return_probability, step):
        self.msg_number = msg_number
        self.return_probability = return_probability
        self.step = step

        self.generator = Generator(a, b)
        self.handler = Handler(mu, sigma)

    def step_principle(self):
        max_length = 0
        now_length = 0
        processed_msgs = 0
        self.handler.free = True

        now_time = self.step
        generation_time = self.generator.get_time_interval()
        prev_generation_time = 0
        handling_time = 0

        while processed_msgs < self.msg_number:

            if now_time > generation_time:
                now_length += 1

                if max_length < now_length:
                    max_length = now_length

                prev_generation_time = generation_time
                generation_time += self.generator.get_time_interval()

            if now_time > handling_time:
                if now_length > 0:
                    was_free = self.handler.free

                    if self.handler.free:
                        self.handler.free = False
                    else:
                        processed_msgs += 1
                        now_length -= 1

                        now_return_probability = random()

                        if now_return_probability <= self.return_probability:
                            now_length += 1

                    if was_free:
                        handling_time = prev_generation_time + \
                                        self.handler.get_time_interval()
                    else:
                        handling_time += self.handler.get_time_interval()

                else:
                    self.handler.free = True

            now_time += self.step
        
        return max_length
    
    def eventful_principle(self):
        max_length = 0
        now_length = 0
        processed_msgs = 0
        processed = False
        self.handler.free = True

        events = [[self.generator.get_time_interval(), State.generation]]

        while processed_msgs < self.msg_number:
            event = events.pop(0)

            if event[Constants.state] == State.generation:
                now_length += 1

                if max_length < now_length:
                    max_length = now_length

                self.__add_event(events, [event[Constants.time] + \
                                 self.generator.get_time_interval(),
                                 State.generation])

                if self.handler.free:
                    processed = True
            
            if event[Constants.state] == State.handling:
                processed_msgs += 1
                now_return_probability = random()

                if now_return_probability <= self.return_probability:
                    now_length += 1

                processed = True
            
            if processed:
                if now_length > 0:
                    now_length -= 1
                    self.__add_event(events, [event[Constants.time] + \
                                     self.handler.get_time_interval(),
                                     State.handling])
                    self.handler.free = False
                else:
                    self.handler.free = True
                
                processed = False

        return max_length

    def __add_event(self, events, event):
        i = 0

        while i < len(events) and \
              events[i][Constants.time] < event[Constants.time]:
              i += 1

        if 0 < i < len(events):
            events.insert(i - 1, event)
        else:
            events.insert(i, event)
