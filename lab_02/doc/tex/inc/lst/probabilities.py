def __get_factors(self):
    factors = []

    for state in range(self.number_states):
        factors.append([0] * self.number_states)

        for i in range(self.number_states):
            if i != state:
                factors[state][i] = self.intensity_matrix[i][state]
                factors[state][state] += self.intensity_matrix[state][i]
        factors[state][state] *= -1

    return factors
    
def get_limit_probabilities(self):
    factors = self.__get_factors()
    factors[-1] = [1] * self.number_states

    free_numbers = [0] * self.number_states
    free_numbers[-1] = 1

    return linalg.solve(factors, free_numbers)
