def get_time_interval(self):
    random_sum = sum([random() for _ in range(Constants.n)])
    return self.sigma * (random_sum - 6) + self.mu
