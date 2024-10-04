# plan.py

from point import Point
from vector import Vector

class Plan:
    MAX_POINTS = 5
    MAX_VECTORS = 4

    def __init__(self):
        self.points = []
        self.vectors = []
    
    def add_point(self, point: Point):
        if len(self.points) >= self.MAX_POINTS:
            print(f"Não é possível adicionar mais de {self.MAX_POINTS} pontos.")
        else:
            self.points.append(point)
    
    def add_vector(self, vector: Vector):
        if len(self.vectors) >= self.MAX_VECTORS:
            print(f"Não é possível adicionar mais de {self.MAX_VECTORS} vetores.")
        else:
            self.vectors.append(vector)
