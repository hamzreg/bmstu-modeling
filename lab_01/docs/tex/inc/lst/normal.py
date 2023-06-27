def __normal_function(self, mu, sigma, x):
    return (1 + erf((x - mu) / sqrt(2 * sigma ** 2))) / 2


def __normal_density(self, mu, sigma, x):
    return (1 / (sigma * sqrt(2 * pi))) * \
           exp(-((x - mu) ** 2 / (2 * sigma ** 2)))
