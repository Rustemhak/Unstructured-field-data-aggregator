from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, fact):
        self.fact = fact

    @abstractmethod
    def __str__(self):
        pass


class FieldName(BaseModel):
    def __str__(self):
        return self.fact.first.capitalize() + ' ' + self.fact.last


class ExploitDate(BaseModel):
    def __str__(self):
        return self.fact.date


class OpenDate(BaseModel):
    def __str__(self):
        return self.fact.date


class Location(BaseModel):
    def __str__(self):
        return self.fact.name


class OilSat(BaseModel):
    def __str__(self):
        if self.fact.object_name and self.fact.num_def:
            return f'object_name: {self.fact.object_name}, num_def: {self.fact.num_def}, value: {self.fact.oil_sat_value}'
        elif self.fact.object_name:
            return f'object_name: {self.fact.object_name}, value: {self.fact.oil_sat_value}'
        elif self.fact.num_def:
            return f'num_def: {self.fact.num_def}, value: {self.fact.oil_sat_value}'
        else:
            return f'value: {self.fact.oil_sat_value}'


class Porosity(BaseModel):
    def __str__(self):
        if self.fact.object_name and self.fact.num_def:
            return f'object_name: {self.fact.object_name}, num_def: {self.fact.num_def}, value: {self.fact.porosity_value}'
        elif self.fact.object_name:
            return f'object_name: {self.fact.object_name}, value: {self.fact.porosity_value}'
        elif self.fact.num_def:
            return f'num_def: {self.fact.num_def}, value: {self.fact.porosity_value}'
        else:
            return f'value: {self.fact.porosity_value}'
