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
                self.__add_event(events, 
                                 [event[Constants.time] + \
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
