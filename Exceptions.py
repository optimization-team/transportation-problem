class AlternatingOptima(Exception):
    def __init__(self, solution):
        super().__init__("Alternating optima detected!")
        self.solution = solution


class InfeasibleSolution(Exception):
    def __init__(self):
        super().__init__("Infeasible solution, method is not applicable!")


class InvalidRightVector(Exception):
    def __init__(self, vector):
        super().__init__("Provided the invalid B vector")
        self.vector = vector


class DivergenceException(Exception):
    def __init__(self, point):
        super().__init__("Method fall into divergent point.")
        self.point = point
