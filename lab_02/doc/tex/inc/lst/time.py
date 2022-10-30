def __get_derivatives(self, probabilities, time, factors):
    derivatives = [0] * self.number_states

    for state in range(self.number_states):
        for i, probability in enumerate(probabilities):
            derivatives[state] += factors[state][i] * probability

    return derivatives
    
def get_stabilization_time(self, limit_probabilities):
    time = arange(0, Constants.max_time, Constants.time_delta)
    
    start_probabilities = [0] * self.number_states
    start_probabilities[0] = 1

    factors = self.__get_factors()

    integrated_probabilities = 
        transpose(odeint(self.__get_derivatives, 
                         start_probabilities, 
                         time, args=(factors,)))

    stabilization_time = []

    for state in range(self.number_states):
        probabilities = integrated_probabilities[state]

        for i, probability in enumerate(probabilities):
            if abs(limit_probabilities[state] - probability) < Constants.eps:
                stabilization_time.append(time[i])
                break

            if i == len(probabilities) - 1:
                stabilization_time.append(0)

    return stabilization_time
