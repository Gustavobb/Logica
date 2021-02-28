# macielcalebe
import sys
import re

operators = ['+', '-']

def raise_error(error: str) -> None:
    raise ValueError(error)
    exit(1)

def extract_clean_input(input_argv: str) -> list:
    ret_clean_input = []
    tmp = list(filter(None, re.split('(\d+)', input_argv)))
    for i in tmp: 
        s = i.replace(" ", "")
        if s != '':
            ret_clean_input += [s]

    print(ret_clean_input)
    return ret_clean_input

def extract_operators_and_numbers_of_input(input_argv: list) -> list:
    ret_operators = []
    ret_numbers = []
    found_number = False
    found_operator = False

    for token in input_argv:

        if not token.isnumeric():
            if token in operators and not found_operator:
                ret_operators += [token]
                found_operator = True
                found_number = False

            else:
                raise_error("invalid operators")
        
        elif not found_number:
            ret_numbers += [token]
            found_number = True
            found_operator = False
        
        else:
            raise_error("double numbers")

    return ret_operators, ret_numbers

def invalid_operand_test(input_argv: list) -> None:
    if not input_argv[0].isnumeric(): raise_error("first element must be int")
    elif not input_argv[-1].isnumeric(): raise_error("last element must be int")

def main(argv: str) -> int:
    result = 0
    
    argv = extract_clean_input(argv)
    invalid_operand_test(argv)

    operators_in_argv, numbers_in_argv = extract_operators_and_numbers_of_input(argv)

    final_list = [j for i in zip(numbers_in_argv, operators_in_argv) for j in i]
    operation = 1

    for element in final_list:
        #print(element)
        if element == '+': operation = 1
        elif element == '-': operation = -1
        else: result += int(element) * operation

    result += int(numbers_in_argv[-1]) * operation
    print(result)
    return 0

if __name__ == "__main__":
    main(sys.argv[1])