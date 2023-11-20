from TransportationProblem import NorthwestCornerMethod, VogelMethod, RussellMethod
from Exceptions import ImbalancedProblem, InfeasibleSolution
from input_parser import parse_input


def main():
    supply, demand, costs = parse_input("inputs/input1.txt")
    try:
        northwest = NorthwestCornerMethod(supply, demand, costs)
        vogel = VogelMethod(supply, demand, costs)
        russell = RussellMethod(supply, demand, costs)
        northwest.print_initial_table()

        print("-----------------------------")
        print("Northwest Corner rule:")
        print(northwest.solve())
        print("-----------------------------")
        print("Vogel's approximation:")
        print(vogel.solve())
        print("-----------------------------")
        print("Russell's approximation:")
        print(russell.solve())

    except InfeasibleSolution:
        print("The method is not applicable!")
        return
    except ImbalancedProblem:
        print("The problem is not balanced!")
        return


if __name__ == '__main__':
    main()
