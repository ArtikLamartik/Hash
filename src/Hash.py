import random
import shlex
import time
import sys
import os

try:

    EXIT        =  "exit"            # it is used to exit the program
    COMMENT     =  "//"              # it is used to comment a line
    PASS        =  "pass"            # it is used to pass a line
    IMP         =  "#imp"            # it is used to import a module
    INCLUDEVOID =  "#includevoid"    # it is used to include a any function from the file
    SET         =  "set"             # it is used to set a variable
    OUT         =  "out"             # it is used to output
    INP         =  "inp"             # it is used to input
    LOWER       =  "lower"           # it is used to make a string lowercase
    UPPER       =  "upper"           # it is used to make a string uppercase
    FUPPER      =  "fupper"          # it is used to make a string capitalize (first-uppercase)
    LUPPER      =  "lupper"          # it is used to make a string capitalize, but at the end (last-uppercase)
    FLOWER      =  "flower"          # it is used to make a string uncapitalize (first-lowercase), will make the first letter lowercase
    LLOWER      =  "llower"          # it is used to make a string uncapitalize (last-lowercase), will make the last letter lowercase
    REVERSE     =  "reverse"         # it is used to reverse a string
    ADD         =  "add"             # it is used to add
    SUB         =  "sub"             # it is used to subtract
    MUL         =  "mul"             # it is used to multiply
    DIV         =  "div"             # it is used to divide
    FUNC        =  "func"            # it is used to make a function
    CALL        =  "call"            # it is used to call a function
    ABS         =  "abs"             # it is used to make a variable absolute
    ROUND       =  "round"           # it is used to round a float
    RANDOM      =  "random"          # it is used to get a random number beetwen two numbers
    LOOP        =  "loop"            # it is used to loop
    IF          =  "if"              # it is used to check if something is TRUE
    WAIT        =  "wait"            # it is used to wait for a specific time (in seconds)
    STR         =  "str"             # it is used to make a variable a string
    INT         =  "int"             # it is used to make a variable a intiger
    FLT         =  "flt"             # it is used to make a variable a float
    BOL         =  "bol"             # it is used to make a variable a boolean
    ARG         =  "arg"             # it is used to get the arguments from running the code
    ISSTR       =  "isstr"           # it is used to check if a variable is an string
    ISINT       =  "isint"           # it is used to check if a variable is an integer
    ISFLT       =  "isflt"           # it is used to check if a variable is an float
    ISBOL       =  "isbol"           # it is used to check if a variable is an boolean

    try:
        if sys.argv[1].endswith(".hash"):
            filename = sys.argv[1]
        else:
            print("Invalid File Name (it does not end with .hash)")
            exit(1)
    except:
        print("Invalid File Name (not provided)")
        exit(1)

    alltokens = []
    variables = {"pi": "3.14159", "e": "2.71828", "inf": "∞"}
    functions = {}
    allowed_imports = ["sys", "system"]
    imports = []

    try:
        with open(filename, "r") as hashfile:
            allcode = hashfile.readlines()
            for line in allcode:
                if COMMENT in line:
                    line = line[: line.index(COMMENT)]
                tokens = shlex.split(line)
                for token in tokens:
                    alltokens.append(token)
                alltokens.append("\n")
    except:
        print("File not found")
        exit(1)

    def interpret_vars(input_str):
        for name, value in variables.items():
            placeholder = f"[{name}]"
            if placeholder in input_str:
                input_str = input_str.replace(placeholder, str(value))
        if input_str.startswith("[") and input_str.endswith("]"):
            return None
        return input_str

    def remove_brackets(vars_name):
        return vars_name.strip("[]")

    def isvar(var_name):
        return var_name.startswith("[") and var_name.endswith("]")

    sys.set_int_max_str_digits(1000000000)

    global ending
    global starting
    global call_i
    global counter
    global end
    global strt

    counter = 1

    i = 0
    while i < len(alltokens):
        token = alltokens[i]
        if token.lower() == EXIT:
            exit(0)
        elif token.lower() == "sys" or token.lower() == "system":
            if any(x.lower() in ["sys", "system"] for x in imports):
                if alltokens[i + 1].lower() == "run":
                    try:
                        os.system(alltokens[i + 2])
                    except:
                        pass
                    i += 2
                elif alltokens[i + 1].lower() == "read":
                    var_name = alltokens[i + 2]
                    file_name = alltokens[i + 3]
                    with open(file_name, "r") as file:
                        variables[remove_brackets(var_name)] = file.read()
                    i += 3
                elif alltokens[i + 1].lower() == "write":
                    var_name = alltokens[i + 2]
                    file_name = alltokens[i + 3]
                    with open(file_name, "w") as file:
                        message = interpret_vars(var_name)
                        message = message.replace("/n", "\n").replace("/t", "\t")
                        file.write(str(message))
                    i += 3
                elif alltokens[i + 1].lower() == "append":
                    file_name = alltokens[i + 2]
                    with open(file_name, "a") as file:
                        message = interpret_vars(alltokens[i + 3])
                        message = message.replace("/n", "\n").replace("/t", "\t")
                        file.write(str(message))
                    i += 3
                elif alltokens[i + 1].lower() == "delf":
                    file_name = alltokens[i + 2]
                    os.remove(file_name)
                    i += 2
                elif alltokens[i + 1].lower() == "arg":
                    var_name = alltokens[i + 2]
                    arg_num = alltokens[i + 3]
                    var = remove_brackets(var_name)
                    try:
                        variables[var] = sys.argv[int(arg_num) + 1]
                    except:
                        pass
                    i += 3
            else:
                print("System module not imported")
                exit(1)
        elif token.lower() == INCLUDEVOID:
            try:
                with open(alltokens[i + 1], "r") as hashfile:
                    file_code = hashfile.read()
                    file_code = shlex.split(file_code)
                    while True:
                        try:
                            start_index = file_code.index("func")
                            end_index = file_code.index("}")
                            func_code = file_code[start_index:end_index]
                            alltokens[i+1:i+1] = func_code
                            alltokens.insert(i+1, "{")
                            alltokens.insert(i+2+len(func_code), "}")
                            file_code = file_code[end_index+1:]
                        except ValueError:
                            break
            except FileNotFoundError:
                print("File not found")
                exit(1)
            i += 1
        elif token.lower() == PASS:
            pass
        elif token.lower() == SET:
            var_name = alltokens[i + 1]
            if alltokens[i + 2] == "=":
                value = interpret_vars(alltokens[i + 3])
                variables[remove_brackets(var_name)] = value
            i += 3
        elif token.lower() == OUT:
            output = interpret_vars(alltokens[i + 1])
            print(
                output,
                end=interpret_vars(alltokens[i + 2]).replace("\\n", "\n").replace("/n", "\n"),
                flush=True,
            )
            i += 2
        elif token.lower() == WAIT:
            time.sleep(float(interpret_vars(alltokens[i + 1])))
            i += 1
        elif token.lower() == IMP:
            if alltokens[i + 1] in allowed_imports:
                imports.append(alltokens[i + 1])
            else:
                print("Invalid Import")
                exit(1)
            i += 1
        elif token.lower() == ISINT:
            var_name = alltokens[i + 1]
            number = alltokens[i + 2]
            var_name = remove_brackets(var_name)
            try:
                number = int(interpret_vars(number))
                variables[var_name] = "TRUE" if isinstance(number, int) else "FALSE"
            except ValueError:
                variables[var_name] = "FALSE"
            except:
                pass
            i += 2
        elif token.lower() == ISFLT:
            var_name = alltokens[i + 1]
            number = alltokens[i + 2]
            var_name = remove_brackets(var_name)
            try:
                number = float(interpret_vars(number))
                variables[var_name] = "TRUE" if isinstance(number, float) else "FALSE"
            except ValueError:
                variables[var_name] = "FALSE"
            except:
                pass
            i += 2
        elif token.lower() == ISSTR:
            var_name = alltokens[i + 1]
            number = alltokens[i + 2]
            var_name = remove_brackets(var_name)
            try:
                number = str(interpret_vars(number))
                variables[var_name] = "TRUE" if isinstance(number, str) else "FALSE"
            except ValueError:
                variables[var_name] = "FALSE"
            except:
                pass
            i += 2
        elif token.lower() == ISBOL:
            var_name = alltokens[i + 1]
            number = alltokens[i + 2]
            var_name = remove_brackets(var_name)
            try:
                number = interpret_vars(number)
                variables[var_name] = str(number == "TRUE" or number == "TRUE").upper()
            except:
                variables[var_name] = "FALSE"
            i += 2
        elif token.lower() == INT:
            var_name = alltokens[i + 1]
            try:
                number = float(interpret_vars(var_name))
                if number.is_integer():
                    variables[remove_brackets(var_name)] = int(number)
                else:
                    variables[remove_brackets(var_name)] = number
            except:
                pass
            i += 1
        elif token.lower() == STR:
            var_name = alltokens[i + 1]
            number = alltokens[i + 2]
            try:
                variables[remove_brackets(var_name)] = str(interpret_vars(var_name))
            except:
                pass
            i += 1
        elif token.lower() == FLT:
            var_name = alltokens[i + 1]
            try:
                variables[remove_brackets(var_name)] = float(interpret_vars(var_name))
            except:
                pass
            i += 1
        elif token.lower() == BOL:
            var_name = alltokens[i + 1]
            try:
                value = interpret_vars(var_name).strip().lower()
                if value == "true" or value == "false":
                    variables[remove_brackets(var_name)] = str(value == "true").upper()
            except:
                pass
            i += 1
        elif token.lower() == ADD:
            var_name = alltokens[i + 1]
            if alltokens[i + 2] != "=":
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Missing Equal Sign. Line {index+1}")
                        exit(1)
            var_name = remove_brackets(var_name)
            val1 = interpret_vars(alltokens[i + 3])
            val2 = interpret_vars(alltokens[i + 4])
            try:
                variables[var_name] = int(val1) + int(val2)
            except ValueError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for ADD. Line {index+1}")
                        exit(1)
            i += 4
        elif token.lower() == SUB:
            var_name = alltokens[i + 1]
            if alltokens[i + 2] != "=":
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Missing Equal Sign. Line {index+1}")
                        exit(1)
            var_name = remove_brackets(var_name)
            val1 = interpret_vars(alltokens[i + 3])
            val2 = interpret_vars(alltokens[i + 4])
            try:
                variables[var_name] = int(val1) - int(val2)
            except ValueError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for SUB. Line {index+1}")
                        exit(1)
            i += 4
        elif token.lower() == MUL:
            var_name = alltokens[i + 1]
            if alltokens[i + 2] != "=":
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Missing Equal Sign. Line {index+1}")
                        exit(1)
            var_name = remove_brackets(var_name)
            val1 = interpret_vars(alltokens[i + 3])
            val2 = interpret_vars(alltokens[i + 4])
            try:
                variables[var_name] = float(val1) * float(val2)
            except ValueError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for MUL. Line {index+1}")
                        exit(1)
            i += 4
        elif token.lower() == DIV:
            var_name = alltokens[i + 1]
            if alltokens[i + 2] != "=":
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Missing Equal Sign. Line {index+1}")
                        exit(1)
            var_name = remove_brackets(var_name)
            val1 = interpret_vars(alltokens[i + 3])
            val2 = interpret_vars(alltokens[i + 4])
            try:
                if float(val1) % float(val2) == 0:
                    variables[var_name] = int(float(val1) / float(val2))
                else:
                    variables[var_name] = float(val1) / float(val2)
            except ValueError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for DIV. Line {index+1}")
                        exit(1)
            except ZeroDivisionError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Division by zero. Line {index+1}")
                        exit(1)
            i += 4
        elif token.lower() == LOWER:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = variables[var_name].lower()
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for LOWER. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == UPPER:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = variables[var_name].upper()
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for UPPER. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == FUPPER:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = variables[var_name].capitalize()
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for FUPPER. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == LUPPER:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = (
                    variables[var_name][:-1] + variables[var_name][-1].upper()
                )
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for LUPPER. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == FLOWER:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = (
                    variables[var_name][0].lower() + variables[var_name][1:]
                )
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for FLOWER. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == LLOWER:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = (
                    variables[var_name][:-1] + variables[var_name][-1].lower()
                )
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for LLOWER. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == REVERSE:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = variables[var_name][::-1]
            except AttributeError:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for REVERSE. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == INP:
            user_input = input(">> ")
            if alltokens[i + 1] == "str":
                variables[remove_brackets(alltokens[i + 2])] = str(user_input)
            elif alltokens[i + 1] == "int":
                try:
                    variables[remove_brackets(alltokens[i + 2])] = int(user_input)
                except ValueError:
                    print("Error: Invalid input. Expected an integer.")
                    exit(1)
            elif alltokens[i + 1] == "flt":
                try:
                    user_input = user_input.replace(",", ".")
                    variables[remove_brackets(alltokens[i + 2])] = float(user_input)
                except ValueError:
                    print("Error: Invalid input. Expected a float.")
                    exit(1)
            elif alltokens[i + 1] == "bol":
                if user_input.strip() == "TRUE":
                    variables[remove_brackets(alltokens[i + 2])] = "TRUE"
                elif user_input.strip() == "FALSE":
                    variables[remove_brackets(alltokens[i + 2])] = "FALSE"
                else:
                    print("Error: Invalid input. Expected a boolean.")
                    exit(1)
            i += 2
        elif token.lower() == FUNC:
            func_name = alltokens[i + 1]
            start_index = alltokens.index("(", i)
            end_index = alltokens.index(")", start_index)
            func_vars = alltokens[start_index + 1 : end_index]
            code = ""
            bracket_count = 0
            for j in range(i + 3, len(alltokens)):
                if alltokens[j] == "{":
                    bracket_count += 1
                elif alltokens[j] == "}":
                    bracket_count -= 1
                    if bracket_count == 0:
                        break
                else:
                    code += alltokens[j] + " "
            functions[func_name] = str(func_vars) + " | " + str(i) + " | " + str(j + 1)
            i = j + 1
        elif token.lower() == CALL:
            func_name = alltokens[i + 1]
            start_index = alltokens.index("(", i)
            end_index = alltokens.index(")", start_index)
            func_vars = alltokens[start_index + 1 : end_index]
            for var in func_vars:
                func_vars[func_vars.index(var)] = interpret_vars(var)
            if func_name in functions:
                inputs = functions[func_name].split(" | ")[0]
                starting = int(functions[func_name].split(" | ")[1])
                ending = int(functions[func_name].split(" | ")[2])
                code_list = alltokens[starting:ending]
                code_list = [x for x in code_list if x != "\n"]
            else:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Function not found. Line {index+1}")
                        exit(1)
            try:
                if len(
                    code_list[code_list.index("(") + 1 : code_list.index(")")]
                ) != len(func_vars):
                    for index, line in enumerate(allcode):
                        if line.startswith(alltokens[i]):
                            print(
                                f"Error: Invalid number of arguments on line {index+1}, expected {len(code_list[code_list.index('(')+1:code_list.index(')')])}, got {len(func_vars)}."
                            )
                            exit(1)
                for k in range(
                    len(code_list[code_list.index("(") + 1 : code_list.index(")")])
                ):
                    variables[
                        code_list[code_list.index("(") + 1 : code_list.index(")")][k]
                    ] = func_vars[k]
                call_i = i
                i = starting + 4 + len(func_vars)
            except:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Function not found. Line {index+1}")
                        exit(1)
        elif token.lower() == ABS:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                variables[var_name] = abs(variables[var_name])
            except:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for ABS. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == ROUND:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                if variables[var_name].is_integer():
                    variables[var_name] = int(variables[var_name])
                elif isinstance(variables[var_name], float):
                    vart2 = variables[var_name] * 2
                    if vart2.is_integer():
                        variables[var_name] = int(variables[var_name] - 0.5)
                    else:
                        variables[var_name] = round(float(variables[var_name]))
            except:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for ROUND. Line {index+1}")
                        exit(1)
            i += 1
        elif token.lower() == RANDOM:
            var_name = alltokens[i + 1]
            var_name = remove_brackets(var_name)
            try:
                if int(alltokens[i + 3]) > int(alltokens[i + 4]):
                    alltokens[i + 3], alltokens[i + 4] = (
                        alltokens[i + 4],
                        alltokens[i + 3],
                    )
                if alltokens[i + 2] == "(" and alltokens[i + 5] == ")":
                    try:
                        if isvar(alltokens[i + 3]) and not isvar(alltokens[i + 4]):
                            variables[var_name] = random.randint(
                                int(interpret_vars(alltokens[i + 3])),
                                int(alltokens[i + 4]),
                            )
                        elif not isvar(alltokens[i + 3]) and isvar(alltokens[i + 4]):
                            variables[var_name] = random.randint(
                                int(alltokens[i + 3]),
                                int(interpret_vars(alltokens[i + 4])),
                            )
                        else:
                            variables[var_name] = random.randint(
                                int(interpret_vars(alltokens[i + 3])),
                                int(interpret_vars(alltokens[i + 4])),
                            )
                    except:
                        variables[var_name] = random.randint(
                            int(alltokens[i + 3]), int(alltokens[i + 4])
                        )
            except:
                for index, line in enumerate(allcode):
                    if line.startswith(alltokens[i]):
                        print(f"Error: Invalid Data Type for RANDOM. Line {index+1}")
                        exit(1)
            i += 5
        elif token.lower() == LOOP:
            counter = alltokens[i + 1]
            if isvar(counter):
                counter = interpret_vars(counter)
                try:
                    counter = int(counter) - 1
                    strt = i + 2
                    end = alltokens.index("}", strt)
                    if counter > -1:
                        i = strt
                    else:
                        i = end + 1
                except:
                    if counter.lower() == "true":
                        counter = -1
                        strt = i + 2
                        end = alltokens.index("}", strt)
                        if counter != -1:
                            i = strt + 1
                    elif counter.lower() == "false":
                        strt = i + 2
                        end = alltokens.index("}", strt)
                        i = end + 1
                    else:
                        for index, line in enumerate(allcode):
                            if line.startswith(alltokens[i]):
                                print(
                                    f"Error: Invalid Data Type for LOOP. Line {index+1}"
                                )
                                exit(1)
            else:
                try:
                    counter = abs(int(counter)) - 1
                    strt = i + 2
                    end = alltokens.index("}", strt)
                    if counter > -1:
                        i = strt
                    else:
                        i = end + 1
                except:
                    if counter.lower() == "true":
                        counter = -1
                        strt = i + 2
                        end = alltokens.index("}", strt)
                        if counter == -1:
                            i = strt
                    elif counter.lower() == "false":
                        strt = i + 2
                        end = alltokens.index("}", strt)
                        i = end + 1
                    else:
                        for index, line in enumerate(allcode):
                            if line.startswith(alltokens[i]):
                                print(
                                    f"Error: Invalid Data Type for LOOP. Line {index+1}"
                                )
                                exit(1)
        elif token.lower() == IF:
            op_1 = alltokens[i + 1]
            oprr = alltokens[i + 2]
            op_2 = alltokens[i + 3]
            try:
                if oprr == "==":
                    if interpret_vars(op_1) == interpret_vars(op_2):
                        srt = i + 5
                        ed = alltokens.index("}", srt) + 2
                        i = srt
                    else:
                        srt = i + 6
                        ed = alltokens.index("}", srt) + 2
                        i = ed
                elif oprr == "!=":
                    if interpret_vars(str(op_1)) != interpret_vars(str(op_2)):
                        srt = i + 5
                        ed = alltokens.index("}", srt) + 2
                        i = srt
                    else:
                        srt = i + 6
                        ed = alltokens.index("}", srt) + 2
                        i = ed
                elif oprr == ">>":
                    if interpret_vars(str(op_1)) > interpret_vars(str(op_2)):
                        srt = i + 5
                        ed = alltokens.index("}", srt) + 1
                        i = srt
                    else:
                        srt = i + 6
                        ed = alltokens.index("}", srt) + 2
                        i = ed
                elif oprr == "<<":
                    if interpret_vars(str(op_1)) < interpret_vars(str(op_2)):
                        srt = i + 5
                        ed = alltokens.index("}", srt) + 1
                        i = srt
                    else:
                        srt = i + 6
                        ed = alltokens.index("}", srt) + 2
                        i = ed
                elif oprr == ">=":
                    if interpret_vars(str(op_1)) >= interpret_vars(str(op_2)):
                        srt = i + 5
                        ed = alltokens.index("}", srt) + 1
                        i = srt
                    else:
                        srt = i + 6
                        ed = alltokens.index("}", srt) + 2
                        i = ed
                elif oprr == "<=":
                    if interpret_vars(str(op_1)) <= interpret_vars(str(op_2)):
                        srt = i + 5
                        ed = alltokens.index("}", srt) + 1
                        i = srt
                    else:
                        srt = i + 6
                        ed = alltokens.index("}", srt) + 2
                        i = ed
            except Exception as e:
                print(f"How did i get an error here? {e}")
                exit(1)
        elif token.strip() != "" and token != "\n" and token != "}":
            for index, line in enumerate(allcode):
                if line.startswith(alltokens[i]):
                    print(f"Invalid Command on line {index+1}: {alltokens[i]}")
                    exit(1)
        try:
            if i == ending - 2:
                i = call_i
                param_name = code_list[code_list.index("(") + 1 : code_list.index(")")][
                    k
                ]
                if param_name in func_vars:
                    if not isvar(param_name):
                        del variables[param_name]
                    else:
                        variables[param_name] = None
        except:
            pass
        try:
            if counter != 0:
                if i == end:
                    i = strt
                    try:
                        if counter.lower() == "true":
                            pass
                        elif counter.lower() == "false":
                            pass
                    except:
                        counter -= 1
        except:
            pass
        i += 1

except KeyboardInterrupt:
    sys.exit(0)
except:
    sys.exit(1)