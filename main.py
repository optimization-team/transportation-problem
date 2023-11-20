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

        solution1 = northwest.solve()
        solution2 = vogel.solve()
        solution = russell.solve()
        print("-----------------------------")
        print("Northwest Corner rule:")
        print(solution1)
        print("-----------------------------")
        print("Vogel's approximation:")
        print(solution2)
        print("-----------------------------")
        print("Russell's approximation:")
        print(solution)

    except InfeasibleSolution:
        print("The problem does not have solution!")
        return
    except ImbalancedProblem:
        print("The problem is not balanced!")
        return


if __name__ == '__main__':
    main()
