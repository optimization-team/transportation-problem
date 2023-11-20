from TransportationProblem import Transportation, TransportationSolution
from Exceptions import InfeasibleSolution
from input_parser import parse_input


def main():
    supply, demand, costs = parse_input("inputs/input1.txt")

    try:
        transportation = Transportation(supply, demand, costs)
        transportation.print_initial_table()
        solution = transportation.russell_method()
        solution1 = transportation.northwest_corner_method()
        solution2 = transportation.vogel_method()
        print("Northwest Corner rule:\n", solution1)
        print("Vogel's approximation:\n", solution2)
    except InfeasibleSolution:
        print("The problem does not have solution!")
        return


if __name__ == '__main__':
    main()