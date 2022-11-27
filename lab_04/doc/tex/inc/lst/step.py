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
