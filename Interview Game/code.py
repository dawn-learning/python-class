from enum import Enum
from overriden_prints import *

class Status(Enum):
    COMPLETED = 0
    PAUSED = 1
    CONTINUING = 2

class Code():
    def __init__(self, code : str, DEBUG : bool = False) -> None:

        self.actions : list[dict]= []
        self.current = 0
        self.variables = {}

        self.DEBUG = DEBUG

        if len(code) < 1:
            self.current_status = Status.COMPLETED
            return

        self.current_status = Status.CONTINUING
        self._code : list[CodeSegment] = [CodeSegment(code, self)]
        self._update_active()
        self.run_to_pause_or_end()

    def __str__(self) -> str:
        output = ""
        for i in range(len(self.actions)):
            output += "\n"
            if self.current == i: output += "> "
            output += str(self.actions[i])
        status = Status.COMPLETED if self.is_completed() else Status.PAUSED
        return "\n|| Current code content ||" + output + f"\n|| Status = {status} ||"

    def next_line(self, user_input = None):
        if len(self.actions) > self.current:
            output = self.actions[self.current]
            self.current += 1
            return output
        if user_input == None:
            if self.current_status == Status.PAUSED:
                return Status.PAUSED
            return None
        status = self.run_to_pause_or_end(user_input=user_input)
        if len(self.actions) > self.current:
            return self.next_line()
        if status == Status.PAUSED: return Status.PAUSED
        return Status.COMPLETED

    def _update_active(self) -> None:
        self._active_code : CodeSegment = self._code[len(self._code)-1]
        if self.DEBUG: print("New focused line:")
        if self.DEBUG: print(f" {self._active_code.position}/{len(self._active_code.lines)}")
        if self.DEBUG: print(f" {self._active_code.lines[self._active_code.position]}")

    def _indent(self, indent_code : list[str]) -> None:
        self._code.append(CodeSegment(indent_code, self))
        self._update_active()

    def change_DEBUG(self, DEBUG : bool) -> None:
        self.DEBUG = DEBUG

    def _parse_next_line(self) -> Status:
        self._active_code.next()
        while self._active_code.completed:
            if self.pop() == Status.COMPLETED:
                return self._updated_status(Status.COMPLETED)
        return self._updated_status(Status.CONTINUING)

    def _is_if_statement(self):
        return self._active_code.is_if_statement()

    def pop(self) -> Status:
        self._code.pop()
        if self._code == []:
            return self._updated_status(Status.COMPLETED)
        self._update_active()
        return self._updated_status(Status.CONTINUING)

    def find_next_not_indented(self) -> Status:
        if self._active_code.find_next_not_indented() == Status.COMPLETED:
            return self.pop()
        return self._updated_status(Status.CONTINUING)

    def run_if_statement(self, boolean : bool):
        result = self._active_code.run_if_statement(boolean)
        if result == None: return
        if not type(result) == CodeSegment:
            raise Exception(f"Result should be a None or a CodeSegment\n result = {result}")
        self._indent(result)

    def replace_input_with(self, user_input):
        return self._active_code.replace_input_with(user_input)

    def is_completed(self):
        return self._code == []

    def detect_pause(self):
        return self._active_code.detect_pause()

    def _updated_status(self, status : Status):
        self.current_status = status
        return status

    def run_to_pause_or_end(self, user_input : str = None):
        DEBUG = False
        def check_functions(segment):
            for function in [print_character_dialogue, print_player_options]:
                if segment.check_for_and_run_function(function):
                    return True
            return False
        
        if self.is_completed(): 
            return self._updated_status(Status.COMPLETED)

        if user_input:
            self.replace_input_with(user_input)
        while not self.is_completed():
            try:
                self._active_code.get_line()
            except:
                print(len(self._code))
                print(len(self._active_code.lines))
                print(self._active_code.position)

            if self.detect_pause():
                return self._updated_status(Status.PAUSED)
            elif check_functions(self._active_code): 
                self._parse_next_line()
                continue
            elif (result := self._is_if_statement()) != None:
                if DEBUG: print("is an if statement")
                if (result := self._active_code.run_if_statement(result)) != None:
                    self._indent(result)
                continue
            else:
                if DEBUG: print(f"if statement result is {result}")
                if DEBUG: print("Assuming must be of another line type")
                self._active_code.other_line_type()
            self._parse_next_line()
        return self._updated_status(Status.COMPLETED)

    def predict_and_convert_to_true_type(self, unknown : str):
        if type(unknown) != str:
            return unknown
        unknown = unknown.strip()
        if (unknown.startswith("'") and unknown.endswith("'")) or (unknown.startswith('"') and unknown.endswith('"')):
            return str(unknown[1 : -1])
        if "." in unknown:
            try:
                return float(unknown)
            except:
                pass
        try:
            return int(unknown)
        except:
            pass
        if (unknown == "True"): return True
        if (unknown == "False"): return False
        for variable in self.variables.keys():
            if unknown == variable:
                # print(f"Replacing {variable} with {variables[variable]}")
                return self.variables[variable]
        return unknown

    def print_actions(self):
        for a in self.actions:
            print(a)

class CodeSegment():
    def __init__(self, lines : list[str], code : Code, position : int = 0, repeat = False, DEBUG : bool = False) -> None:
        self.lines = lines
        self.position = position
        self.repeat = repeat
        self.DEBUG = DEBUG
        self.completed = False
        self.parent = code

    def check_for_and_run_function(self, function):
        DEBUG = False
        def sort_parameters(full_list):
            def check_if_named(line):
                if "=" not in line:
                    return False
                temp = line[:line.index("=")]
                if "'" in temp or '"' in temp:
                    return False
                return True

            unnamed_parameters = []
            named_parameters = {"actions" : self.parent.actions}
            while len(full_list) > 0:
                input = full_list.pop(0)
                if check_if_named(input):
                    parameter, value = input.split("=")
                    named_parameters[parameter] = self.parent.predict_and_convert_to_true_type(value)
                    continue
                else:
                    unnamed_parameters.append(self.parent.predict_and_convert_to_true_type(input))
            return unnamed_parameters, named_parameters

        # Check if the line contains the function
        function_name = function.__name__
        if DEBUG: print(f"Checking line to see if it calls {function_name}...", end="")
        line = self.lines[self.position]
        if not line.startswith(function_name):
            if DEBUG: print(" Nope")
            return False
        if DEBUG: print(" Yep")
        # Extract the parameters
        full_list = parse_function(line, function_name)
        if DEBUG: print(f" All parameters: [{full_list}]")
        unnamed_parameters, named_parameters = sort_parameters(full_list)
        if DEBUG: print(f" Sorted into unnamed: {unnamed_parameters} and named: {named_parameters}")
        # Run the function
        function(*unnamed_parameters, **named_parameters)
        return True

    def change_DEBUG(self, DEBUG : bool) -> None:
        self.DEBUG = DEBUG

    def next(self) -> None:
        """
        Moves the position to the next line.\n
        - Returns COMPLETED if reaches end of CodeSegment by doing so.\n
        - Returns CONTINUING otherwise.
        """
        self.position += 1
        if self.position >= len(self.lines):
            self.completed = True
            return Status.COMPLETED
        Status.CONTINUING

    def get_line(self) -> str:
        return self.lines[self.position]

    def is_if_statement(self):
        """
        - returns None if not an if statement
        - returns the True/False falue of the statement if is an if statement
        note: if, elif, and else statements all count as a type of if statement for this function's purposes
        """
        def turn_line_into_True_or_False(line : str) -> bool:
            if not line.endswith(":"):
                raise Exception("If statement does not include a semicolon at the end")
            if line.startswith("if"):
                line = line.removeprefix("if")
            elif line.startswith("elif"):
                line = line.removeprefix("elif")
            line = line.removesuffix(":").strip()
            line = self.squish_array(split(line), DEBUG=False)[0]
            if line == None:
                raise Exception('An "if" statement cannot be empty.\n You probably used "=" instead of "==".')
            return line

        line = self.get_line()
        startsw = line.startswith("if")
        if line.startswith("else"):
            if not (line.strip() == "else:"):
                raise Exception('Incorrectly formated "else:"')
            line = "if True:"
        if not (line.startswith("if") or line.startswith("elif")):
            return None
        return turn_line_into_True_or_False(line)

    def run_if_statement(self, boolean):
        if self.DEBUG: print(f"If statement is {boolean}")
        if self.DEBUG: print(f" and line_i is {self.position}")
        if self.DEBUG: print(f" and the line is {print_line(self.lines, self.position)}")
        if boolean:
            # If statement is true
            self.next()
            if self.completed:
                raise Exception("If type statements must have some code under them.")
            # Grab all lines in the if
            indeneted_statements = []
            while(self.lines[self.position].startswith("    ")):
                indeneted_statements.append(self.lines[self.position].removeprefix("    "))
                self.next()
                if self.completed: break
            if self.completed:
                # Return the CodeSegment that was under the if
                return indeneted_statements
            # Skip over any elif or else statements after the if
            while self.lines[self.position].startswith("elif") or self.lines[self.position].startswith("else"):
                self.find_next_not_indented()
                if self.completed: break
            # Return the CodeSegment that was under the if
                # if self.DEBUG: print(f"{len(self.lines)}")
                # if self.DEBUG: print(f"line_i  is {self.position} ({print_line(self.lines, self.position)})")
            return indeneted_statements
        else:
            # If statement is false
            # Skip over all lines in the if
            self.find_next_not_indented()
            return None

    def find_next_not_indented(self) -> Status:
        """
        Moves the position to the next line that is not indented.\n
        - Returns COMPLETED if reaches end of CodeSegment by doing so.\n
        - Returns CONTINUING otherwise.
        """
        # At an if or elif statement
        # +1 moves to first line in the indent (1 line must exist, otherwise error in code editor)
        self.next()
        # Skip over each line with an indent
        while(self.position < len(self.lines) and self.lines[self.position].startswith("    ")):
            if self.next() == Status.COMPLETED:
                # Could have hit end of file
                return Status.COMPLETED
        # self.position should be set to next line not a part of the if or elif satement
        if self.DEBUG: print(f" and the next line not a part of the if is {print_line(self.lines, self.position)}")
        return Status.CONTINUING

    def detect_pause(self):
        line = self.get_line()
        return "input" in line and not ("'" in line or '"' in line)

    def replace_input_with(self, new_content):
        if (type(new_content)) == str:
            new_content = f'"{new_content}"'
        self.lines[self.position] = self.get_line().replace("input()", new_content)

    def other_line_type(self):
        DEBUG = False
        self.lines[self.position] = self.squish_array(split(self.get_line()), DEBUG=DEBUG)[0]

    def squish_array(self, array : list, DEBUG = False):
        if DEBUG: print("\narray is", array)
        for double_operator in ["+=", "-=", "*=", "/="]:
            while (double_operator in array):
                spot = array.index(double_operator)
                array[spot] = double_operator[1]
                array.insert(spot+1, double_operator[0])
                array.insert(spot+1, array[spot-1])
        if DEBUG: print("- double operators", array)
        while ("(" in array):
            parenthesis = []
            parenthesis_added = False
            if DEBUG: print("checking array:", array)
            for i in range(len(array)):
                if array[i] == "(":
                    parenthesis.append(")")
                    if str(parenthesis_added) == "False":
                        parenthesis_added = i
                    if DEBUG: print(f"open parenthesis index = {i}")
                elif array[i] == ")":
                    parenthesis.pop()
                    if DEBUG: print(f"close parenthesis index = {i}")
                if str(parenthesis_added) != "False" and (len(parenthesis) == 0):
                    if DEBUG: print("Detected largest internal array:", array[parenthesis_added+1 : i])
                    result = self.squish_array(array[parenthesis_added+1 : i], DEBUG=DEBUG)
                    array = array[: parenthesis_added] + result + array[i+1:]
                    break
                    # for _ in range(i - parenthesis_added + 1):
                    #     array.pop(parenthesis_added)
                    # array.insert(parenthesis_added, result[0])
        # return
        if DEBUG: print("array (-parenthesis) is", array)
        while len(array) > 1:
            # Error checking
            if (len(array) == 2):
                array == [str(array[0]) + str(array[1])]
                break
            # Order of operations
            for operator in ["*", "/", "+", "-", "and", "or", "==", "="]:
                array, worked = self.check_operator(array, operator)
                if (worked):
                    if DEBUG: print("Doing", operator)
                    if DEBUG and len(array) > 1: print(array)
                    break
        if len(array) == 0: array = [None]
        if DEBUG: print(f"returning array: {array}\n")
        return array

    def check_operator(self, array, operator):
        DEBUG = False
        if operator in array:
            index = array.index(operator)
            left : list = array[index-1]
            if type(left) == str:
                left = left.strip()
            if not operator == "=":
                left = self.parent.predict_and_convert_to_true_type(left)
            right : list = self.parent.predict_and_convert_to_true_type(array[index+1])
            if operator == "*":
                array = array[: index-1] + [left * right] + array[index + 2:]
            elif operator == "/":
                array = array[: index-1] + [left / right] + array[index + 2:]
            elif operator == "+":
                array = array[: index-1] + [left + right] + array[index + 2:]
            elif operator == "-":
                array = array[: index-1] + [left - right] + array[index + 2:]
            elif operator == "and":
                array = array[: index-1] + [left and right] + array[index + 2:]
            elif operator == "or":
                array = array[: index-1] + [left or right] + array[index + 2:]
            elif operator == "==":
                # print(f"left {left} of type {type(left)} is being compared to right {right} of type {type(right)}")
                array = array[: index-1] + [left == right] + array[index + 2:]
            elif operator == "=":
                if DEBUG: print(f"variable {left} is being set to {right} or type {type(right)}")
                self.parent.variables[left] = right
                array = array[: index-1] + array[index + 2:]
            return array, True
        return array, False

def print_line(lines, position):
    return lines[position] if position < len(lines) else "EOF"

def split(text):
    array = [text]
    array_spot = 0
    while (array_spot < len(array)):
        to_deal_with = array.pop(array_spot).strip()
        for text_spot in range(len(to_deal_with)):
            found = False
            for a in ["==", "+=", "-=", "*=", "/=", "(", ")", "*", "=", "+", "/", "or", "and"]:
                if (to_deal_with[text_spot : text_spot + len(a)] == a):
                    before = to_deal_with[0: text_spot]
                    if len(before) > 0:
                        array.append(before)
                        array_spot +=1 
                    array.append(to_deal_with[text_spot : text_spot + len(a)])
                    to_deal_with = to_deal_with[text_spot + len(a) :]
                    found = True
                    break
            if found:
                break
        if len(to_deal_with) > 0:
            array.append(to_deal_with)
        array_spot += 1
        # print(array)
    return array

def parse_function(line, function_name):
    line : str = line.strip().removeprefix(function_name).removesuffix(")").strip().removeprefix("(")
    return [a.strip() for a in line.split(",")]

def load_code(filename : str = "test.py"):
    their_code = []
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if not line: break
            # Removes lines that are not code
            if (line == "\n"): continue
            if line.lstrip().startswith("#"): continue
            if "#" in line:
                line = line[:line.index("#")]
            # Removes import statements
            if "import" in line and not ( "'" in line or '"' in line): continue
            # Appends the rest
            their_code.append(line[:-1])
    return Code(their_code)

if __name__ == "__main__":
    code = load_code()
    running = True
    line = True
    while line:
        line = code.next_line("1")
        print(line)
        if line == Status.COMPLETED: running = False
    print(code)
