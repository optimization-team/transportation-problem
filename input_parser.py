from numpy import matrix


def parse_input(filename: str) -> tuple:
    with open(filename) as file:
        # read the first line as a vector of supply
        supply = list(map(int, file.readline().split()))
        file.readline()
        # read the second line as a vector of demand
        demand = list(map(int, file.readline().split()))
        file.readline()
        # read the rest of the file as a matrix of costs
        costs = list()
        for line in file.readlines():
            costs.append(list(map(int, line.split())))
        return supply, demand, costs
