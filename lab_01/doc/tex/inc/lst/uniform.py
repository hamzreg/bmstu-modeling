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
