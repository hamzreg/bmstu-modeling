def get_sequence(self, digits_number, elements_number):
    sequence = []

    divider = pow(10, digits_number)

    while elements_number:
        number = self.table.read(6)

        if number == '':
            self.table.seek(0)
            number = self.table.read(6)

        number = int(number[:5])

        while number:
            if elements_number:
                random_number = number % divider

                if len(str(random_number)) == digits_number:
                    sequence.append(random_number)
                    elements_number -= 1

                number //= 10
            else:
                return sequence

    return sequence
