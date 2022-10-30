from dataclasses import dataclass
from numpy import linalg, transpose, arange
from scipy.integrate import odeint
import matplotlib.pyplot as plt


@dataclass
class Constants:
    min_number_states = 1
    max_number_states = 10

    max_time = 20
    time_delta = 0.01
    eps = 1e-4


class QSystem:
    def __init__(self, number_states):
        self.intensity_matrix = []
        self.number_states = number_states

    def get_limit_probabilities(self):
        factors = self.__get_factors()
        factors[-1] = [1] * self.number_states

        free_numbers = [0] * self.number_states
        free_numbers[-1] = 1

        return linalg.solve(factors, free_numbers)

    def get_stabilization_time(self, limit_probabilities):
        time = arange(0, Constants.max_time, Constants.time_delta)
    
        start_probabilities = [0] * self.number_states
        start_probabilities[0] = 1

        factors = self.__get_factors()

        integrated_probabilities = transpose(odeint(self.__get_derivatives, 
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

    def plot_charts(self):
        time = arange(0, Constants.max_time, Constants.time_delta)
    
        start_probabilities = [0] * self.number_states
        start_probabilities[0] = 1

        factors = self.__get_factors()

        probabilities = transpose(odeint(self.__get_derivatives, 
                                                    start_probabilities, 
                                                    time, args=(factors,)))

        for state in range(self.number_states):
            plt.plot(time, probabilities[state], label = f'P{state + 1}')

        plt.ylabel('P')
        plt.xlabel("t, с")

        plt.legend()
        plt.grid()
        plt.show()

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

    def __get_derivatives(self, probabilities, time, factors):
        derivatives = [0] * self.number_states

        for state in range(self.number_states):
            for i, probability in enumerate(probabilities):
                derivatives[state] += factors[state][i] * probability

        return derivatives
