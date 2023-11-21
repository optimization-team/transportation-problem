# Programing task 3, Introduction to optimization

## How to test the program on your Transportation Problem
To test the program on your input, input the Transportation Problem into one of the files in [inputs](https://github.com/optimization-team/transportation-problem/tree/main/inputs) folder.
- Enter supply values, separated by space, in one line.
- Enter demand values, separated by space, in one line.
- Enter cost values, line by line.

Specify the name of the file from [inputs](https://github.com/optimization-team/transportation-problem/tree/main/inputs) folder you want to use as an argument in parse_file() function in [main.py](https://github.com/optimization-team/transportation-problem/blob/main/main.py), line 7. Then, run the [main.py](https://github.com/optimization-team/transportation-problem/blob/main/main.py) file.

## Structure of the project
### [inputs](https://github.com/optimization-team/transportation-problem/tree/main/inputs)
Folder, containing 4 different inputs, on which the program was tested.
### [Exceptions.py](https://github.com/optimization-team/transportation-problem/tree/main/Exceptions.py)
File containing Exceptions which Transportation class can raise.
### [TransportationProblem.py](https://github.com/optimization-team/transportation-problem/tree/main/TransportationProblem.py)
The file contains the following classes:
- NorthwestCornerMethod - Northwest Corner method implementation.
- VogelMethod - Vogel method implementation.
- RussellMethod - Russell method implementation.
- Transportation - parent class for all the three methods, used to instantiate and apply the methods uniformly.
- TransportationSolution - class, used to store the solution for a given transportation problem.
### [input_parser.py](https://github.com/optimization-team/transportation-problem/tree/main/input_parser.py)
File containing functions parsing input into format, needed for the Transportation class.
### [main.py](https://github.com/optimization-team/transportation-problem/tree/main/main.py)
File, from which the program can be tested on the input from certain file from [inputs](https://github.com/optimization-team/transportation-problem/tree/main/inputs) folder.
### [requirements.txt](https://github.com/optimization-team/transportation-problem/tree/main/requirements.txt)
Information about assets needed for the program to be executed correctly.
