from random import random
from dataclasses import dataclass


@dataclass
class Constants:
    n = 12


class Handler:
    def __init__(self, mu, sigma):
        self.mu, self.sigma = mu, sigma
        self.free = True

    def get_time_interval(self):
        random_sum = sum([random() for _ in range(Constants.n)])
        return self.sigma * (random_sum - 6) + self.mu
