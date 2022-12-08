class Commission:
    def __init__(self, enrollee_generator, receivers):
        self.enrollee_generator = enrollee_generator
        self.receivers = receivers

    def service_enrollees(self, probabilities):
        received_documents = [0] * 3
        
        self.enrollee_generator.generate_enrollee(0)
        generated_enrollees = 1

        events = [Event(self.enrollee_generator, 
                  self.enrollee_generator.time_next)]

        while generated_enrollees < self.enrollee_generator.number:
            events = sort_events(events)
            event = events.pop(0)

            if isinstance(event.creator, EnrolleeGenerator):
                handler = self.enrollee_generator.choose_handler()

                if handler is not None:
                    handler.set_busy()
                    handler.generate_time(event.time)
                    events.append(Event(handler, handler.time_next))

                self.enrollee_generator.generate_enrollee
                				(event.time)
                generated_enrollees += 1
                events.append(Event(self.enrollee_generator,
                              self.enrollee_generator.time_next))
            elif isinstance(event.creator, Handler):
                handler = event.creator
                handler.set_free()

                type = choose_department_type(probabilities)
                receiver = self.receivers[type]
                receiver.append_enrollee(type + 1)

                if receiver.is_free() and not receiver.queue_empty():
                    department_type = receiver.pop_enrollee()
                    receiver.set_busy()
                    receiver.generate_time(event.time)
                    events.append(Event(receiver, receiver.time_next))
                    received_documents[department_type - 1] += 1
            elif isinstance(event.creator, Receiver):
                receiver = event.creator
                receiver.set_free()

                if not receiver.queue_empty():
                    department_type = receiver.pop_enrollee()
                    receiver.set_busy()
                    receiver.generate_time(event.time)
                    events.append(Event(receiver, receiver.time_next))
                    received_documents[department_type - 1] += 1

        return received_documents
