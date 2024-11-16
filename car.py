# car.py

from point import Point
from vector import Vector
from pprint import pprint

class Car:
    def __init__(self, position: Point, name: str):
        self.position = position  # Current position of the car
        self.speed = Vector(Point(0, 0), Point(0, 0))  # Starting with speed vector (0,0)
        self.name = name  # Name of the car/player
        self.has_lost_turn = False  # Flag to check if the car has lost the turn

    def possible_moves(self):
        """
        Returns a list of possible speed vectors based on the current speed.
        The car can adjust x or y component by +1, -1, or keep them the same.
        Only one component can be adjusted per turn.
        """
        moves = []

        # Current speed components
        dx = self.speed.ponto_b.x
        dy = self.speed.ponto_b.y

        # Keep the same speed
        moves.append(Point(dx, dy))

        # Increase x by 1
        moves.append(Point(dx + 1, dy))

        # Decrease x by 1
        moves.append(Point(dx - 1, dy))

        # Increase y by 1
        moves.append(Point(dx, dy + 1))

        # Decrease y by 1
        moves.append(Point(dx, dy - 1))
         
        return moves

    def update_speed(self, new_speed: Vector):
        """
        Updates the car's speed vector if the new_speed is a valid move.
        If not, the car loses the turn and does not move.
        """
        flag = False
        moves = self.possible_moves()
        for move in moves:
            if move.x == new_speed.ponto_b.x and move.y == new_speed.ponto_b.y:
                flag = True
         
        if flag:
            self.speed = new_speed
        else:
            self.has_lost_turn = True
            print(f"{self.name} entered an invalid speed vector and loses the turn.")

    def move(self):
        """
        Moves the car according to its speed vector if it hasn't lost the turn.
        """
        if not self.has_lost_turn:
            self.position.x += self.speed.ponto_b.x
            self.position.y += self.speed.ponto_b.y
        else:
            # Reset the flag for the next turn
            self.has_lost_turn = False

    def reset_speed_on_collision(self):
        """
        Resets the car's speed to (0,0) if it hits a wall.
        """
        self.speed = Vector(Point(0, 0), Point(0, 0))
        print(f"{self.name} hit a wall and speed is reset to (0,0).")

    def __str__(self):
        return f"Car {self.name} at position ({self.position.x}, {self.position.y}) with speed ({self.speed.ponto_b.x}, {self.speed.ponto_b.y})"
