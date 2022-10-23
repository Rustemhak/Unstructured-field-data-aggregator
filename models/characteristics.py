class FieldName:
    def __init__(self, fact):
        self.fact = fact

    def __str__(self):
        return self.fact.first.capitalize() + ' ' + self.fact.last


class ExploitDate:
    def __init__(self, fact):
        self.fact = fact

    def __str__(self):
        return self.fact.date


class OpenDate:
    def __init__(self, fact):
        self.fact = fact

    def __str__(self):
        return self.fact.date


class Location:
    def __init__(self, fact):
        self.fact = fact

    def __str__(self):
        return self.fact.name
