from TransportationProblem import Transportation
from Exceptions import InfeasibleSolution
from input_parser import parse_input


def main():
    supply, demand, costs = parse_input("inputs/input1.txt")

    try:
        transportation = Transportation(supply, demand, costs)
        transportation.print_initial_table()
        transportation.north_west_corner_method()
    except InfeasibleSolution:
        print("The problem does not have solution!")
        return

if __name__ == '__main__':
    main()