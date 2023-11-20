class ImbalancedProblem(Exception):
    def __init__(self):
        super().__init__("The problem is not balanced!")


class InfeasibleSolution(Exception):
    def __init__(self):
        super().__init__("Infeasible solution, method is not applicable!")
