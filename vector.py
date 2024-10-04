# vector.py

from point import Point

class Vector:
    def __init__(self, ponto_a: Point, ponto_b: Point, name: str = ''):
        self.ponto_a = ponto_a
        self.ponto_b = ponto_b
        self.name = name
