from math import exp, sqrt, erf, pi


class Disribution():
    def get_uniform_function(self, a, b, start, end, step):
        x = start
        args = []
        values = []

        while x < end + step / 2:
            args.append(x)
            values.append(self.__uniform_function(a, b, x))
            x += step
        
        return args, values

    def get_uniform_density(self, a, b, start, end, step):
        x = start
        args = []
        values = []

        while x < end + step / 2:
            args.append(x)
            values.append(self.__uniform_density(a, b, x))
            x += step
        
        return args, values

    def get_normal_function(self, mu, sigma, start, end, step):
        x = start
        args = []
        values = []

        while x < end + step / 2:
            args.append(x)
            values.append(self.__normal_function(mu, sigma, x))
            x += step
        
        return args, values   

    def get_normal_density(self, mu, sigma, start, end, step):
        x = start
        args = []
        values = []

        while x < end + step / 2:
            args.append(x)
            values.append(self.__normal_density(mu, sigma, x))
            x += step
        
        return args, values   

    def __uniform_function(self, a, b, x):
        if x <= a:
            return 0
        elif x > b:
            return 1
        else:
            return (x - a) / (b - a)
    
    def __uniform_density(self, a, b, x):
        if a <= x <= b:
            return 1 / (b - a)
        else:
            return 0

    def __normal_function(self, mu, sigma, x):
        return (1 + erf((x - mu) / sqrt(2 * sigma ** 2))) / 2

    def __normal_density(self, mu, sigma, x):
        return (1 / (sigma * sqrt(2 * pi))) * \
               exp(-((x - mu) ** 2 / (2 * sigma ** 2)))
