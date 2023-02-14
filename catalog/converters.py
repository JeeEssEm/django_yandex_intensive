class PositiveIntegerConverter:
    regex = r'([1-9]\d*)$'

    def to_python(self, number):
        return int(number)

    def to_url(self, number):
        return str(number)
