grid = []

variableDefinitions = {}
functionDefinitions = {}
local_parameters = {}

# Numeric constants.
constants = {
    "dim": -1,
    "myxpos": -1,
    "myypos": -1,
    "mychips": -1,
    "myballoons": -1,
    "balloonshere": -1,
    "chipshere": -1,
    "spaces": -1,
}

# Direction constants
directions = {
    ":left": -1,
    ":right": -1,
    ":front": -1,
    ":back": -1,
    ":around": -1,
    ":up": -1,
    ":down": -1,
}

# "Turn" command-specific direction constants
t_directions = {":left": -1, ":right": -1, ":around": -1}

# Orientation constants
orientations = {":north": -1, ":south": -1, ":east": -1, ":west": -1}

# Prop constants
props = {":balloons": -1, ":chips": -1}


def createVariable(varName: str, value: any) -> bool:
    if varName in variableDefinitions:
        return False

    variableDefinitions[varName] = value

    return True


def modifyVariable(varName: str, newValue: any) -> bool:
    if varName in variableDefinitions:
        variableDefinitions[varName] = newValue

        return True

    return False


# TODO modify createFunction function so it saves the function and the respective variables
def createFunction(funcName: str, variables: list) -> bool:
    if funcName in functionDefinitions:
        return False

    functionDefinitions[funcName] = variables

    return True


def valid_command(n: dict) -> bool:
    if not n["value"]:
        if n["children"]:
            for i in range(len(n["children"])):
                valid = valid_command(n["children"][i])
                if not valid:
                    print(f"Invalid command: {n['children'][i]['value']}")
                    return False
            return True
        print("Invalid syntax: empty parenthesis without subelements.")
        return False
    else:
        return (
            n["value"].split()[0] == "if"
            or n["value"].split()[0] in commands_dict
            or n["value"].split()[0] in functionDefinitions
        )


def valid_numeric_value(n: str) -> bool:
    if n.strip() not in constants and n.strip() not in local_parameters:
        try:
            n = int(n)
        except:
            try:  # checks if n corresponds to a variable that was assigned a numeric value.
                n = int(variableDefinitions[n])
            except:
                print(f"Invalid numeric value: {n}")
                return False
    return True


def valid_t_direction(d: str) -> bool:
    var_value = None

    if d.strip() not in t_directions:
        try:  # Checks if d corresponds to a variable that was assigned a direction constant
            var_value = variableDefinitions[d]
        except:
            print(f"Invalid direction value: '{d}'")
            return False
        if var_value not in t_directions:
            print(f"Invalid direction value: '{d}'")
            return False
    return True


def valid_direction(d: str) -> bool:
    var_value = None

    if d.strip() not in directions:
        try:  # Checks if d corresponds to a variable that was assigned a direction constant
            var_value = variableDefinitions[d]
        except:
            print(f"Invalid direction value: '{d}'")
            return False
        if var_value not in directions:
            print(f"Invalid direction value: '{d}'")
            return False
    return True


def valid_orientation(o: str) -> bool:
    var_value = None

    if o not in orientations:
        try:  # Checks if o corresponds to a variable that was assigned an orientation constant
            var_value = variableDefinitions[o]
        except:
            print(f"Invalid orientation value: '{o}'")
            return False
        if var_value not in orientations:
            print(f"Invalid orientation value: '{o}'")
            return False
    return True


def valid_prop(p: str) -> bool:
    var_value = None

    if p not in props:
        try:  # Checks if p corresponds to a variable that was assigned a prop constant
            var_value = variableDefinitions[p]
        except:
            print(f"Invalid prop value: '{p}'")
            return False
        if var_value not in props:
            print(f"Invalid prop value: '{p}'")
            return False
    return True


def defvar_foo(sentence: list) -> bool:
    """
    Checks if the sentence follows the syntax for
    defvar name n
    where name is the number of the variable to initialize and
    n is a number or a constant.
    """

    if len(sentence) != 3:
        print(
            f"""Invalid variable declaration syntax: {' '.join(sentence)}
Must follow the syntax 'defvar name n'"""
        )
        return False

    v_name = sentence[1]
    v_n = sentence[2]
    n = None

    if not valid_numeric_value(v_n):
        return False
    else:
        if v_n in constants:
            n = constants[v_n]
        else:
            n = int(v_n)
    return createVariable(v_name, n)


def equal_foo(sentence: list) -> bool:
    """
    Checks if the sentence follows the syntax for
    = name n
    where name is the number of the variable to modify and
    n is a number or a constant.
    """
    if len(sentence) != 3:
        print(
            f"""Invalid variable modification syntax: {' '.join(sentence)}
Must follow the syntax '= name n'"""
        )
        return False

    v_name = sentence[1].strip()
    v_n = sentence[2]
    n = None

    if not valid_numeric_value(v_n):
        return False
    else:
        if v_n in constants:
            n = constants[v_n]
        else:
            n = int(v_n)
    return modifyVariable(v_name, n)


def move_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    move n
    syntax.
    n must be a numeric value or a constant.
    """
    if len(sentence) != 2:
        print(
            f"""Invalid 'move' function syntax: {' '.join(sentence)}
Must follow the syntax 'move n'"""
        )
        return False

    return valid_numeric_value(sentence[1])


def skip_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    skip n
    syntax.
    n must be a numeric value or a constant.
    """
    if len(sentence) != 2:
        print(
            f"""Invalid 'skip' function syntax: {' '.join(sentence)}
Must follow the syntax 'skip n'"""
        )
        return False

    return valid_numeric_value(sentence[1])


# TODO check :front direction
def turn_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    turn D
    syntax.
    D must be one of the direction constants specific for the 'turn' function.
    """
    if len(sentence) != 2:
        print(
            f"""Invalid 'turn' function syntax: {' '.join(sentence)}
Must follow the syntax 'turn D'"""
        )
        return False

    return valid_direction(sentence[1])


def face_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    face O
    syntax.
    O must be one of the orientation constants.
    """
    if len(sentence) != 2:
        print(
            f"""Invalid 'face' function syntax: {' '.join(sentence)}
Must follow the syntax 'face O'"""
        )
        return False
    return valid_orientation(sentence[1])


def put_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    put X n
    syntax.
    X must be one of the prop constants.
    n must be a valid numeric value
    """
    if len(sentence) != 3:
        print(
            f"""Invalid 'put' function syntax: {' '.join(sentence)}
Must follow the syntax 'put X n'"""
        )
        return False
    return valid_prop(sentence[1]) and valid_numeric_value(sentence[2])


def pick_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    pick X n
    syntax.
    X must be one of the prop constants.
    n must be a valid numeric value
    """
    if len(sentence) != 3:
        print(
            f"""Invalid 'pick' function syntax: {' '.join(sentence)}
Must follow the syntax 'pick X n'"""
        )
        return False
    return valid_prop(sentence[1]) and valid_numeric_value(sentence[2])


def move_dir_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    move-dir n D
    syntax.
    n must be a valid numeric value
    D must be one of the direction constants.
    """
    if len(sentence) != 3:
        print(
            f"""Invalid 'move-dir' function syntax: {' '.join(sentence)}
Must follow the syntax 'move-dir n D'"""
        )
        return False
    n = sentence[1]
    d = sentence[2]
    return valid_numeric_value(n) and (valid_orientation(d) or valid_direction(d))


def run_dirs_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    run-dirs Ds
    syntax.
    Ds is a non-empty list of directions.
    """
    if len(sentence) <= 1:
        print(
            f"""Invalid 'run-dirs' function syntax: {' '.join(sentence)}
Must give a non-empty list of directions.'"""
        )
        return False

    for d in sentence[1:]:
        if not valid_direction(d):
            return False
    return True


def move_face_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    move-face n O
    syntax.
    n must be a valid numeric value
    O must be one of the orientation constants.
    """
    if len(sentence) != 3:
        print(
            f"""Invalid 'move-face' function syntax: {' '.join(sentence)}
Must follow the syntax 'move-face n O'"""
        )
        return False

    n = sentence[1]
    o = sentence[2]

    return valid_numeric_value(n) and valid_orientation(o)


def null_foo(sentence: list) -> bool:
    """
    Verifies whether a sentence follows a valid
    null syntax.
    null must not have any arguments.
    """
    if len(sentence) != 1:
        print(
            f"""Invalid 'null' function syntax: {' '.join(sentence)}
The 'null' function must not have any arguments."""
        )
        return False
    return True


commands_dict = {
    "defvar": defvar_foo,
    "=": equal_foo,
    "move": move_foo,
    "skip": skip_foo,
    "turn": turn_foo,
    "face": face_foo,
    "put": put_foo,
    "pick": pick_foo,
    "move-dir": move_dir_foo,
    "run-dirs": run_dirs_foo,
    "move-face": move_face_foo,
    "null": null_foo,
}


def facing_bool(sentence: list) -> bool:
    if len(sentence) == 2 and valid_orientation(sentence[1]):
        return True

    return False


def blocked_bool(sentence: list) -> bool:
    if len(sentence) == 1:
        return True

    return False


def canPut_bool(sentence: list) -> bool:
    if len(sentence) == 3:
        if sentence[1] == "chips" or sentence[1] == "balloons":
            if valid_numeric_value(sentence[2]):
                return True

    return False


def canPick_bool(sentence: list) -> bool:
    return canPut_bool(sentence)


def canMove_bool(sentence: list) -> bool:
    return facing_bool(sentence)


def isZero_bool(sentence: list) -> bool:
    if len(sentence) != 2:
        print("The isZero? boolean receives only one parameter.")
        return False
    if not valid_numeric_value(sentence[1]):
        return False
    return True


def not_bool(sentence: list, childSentence: list) -> bool:
    if len(sentence) != 1:
        print("'not' operator must not have parameters outside of parenthesis.")
        return False
    if not childSentence[0]["value"].split()[0] in bool_dict:
        print(f"Invalid boolean value: '{childSentence[0]['value']}'")
        return False
    return True


bool_dict = {
    "facing?": facing_bool,
    "blocked?": blocked_bool,
    "can-put?": canPut_bool,
    "can-pick?": canPick_bool,
    "can-move?": canMove_bool,
    "iszero?": isZero_bool,
    "not": not_bool,
}

# TODO crear el diccionario con las estructuras de control del lenguaje (repeat, repeatNTimes) y
# una función respectiva para cada uno que verifique que los parámetros dados sean sintácticamente válidos.


def if_comm(sentence: list, childSentence: list) -> bool:
    if len(sentence) != 1:
        print("Invalid sentence length for if operator.")
        return False
    if 1 > len(childSentence):
        print("Too few arguments for the 'if' conditional.")
        return False
    if not childSentence[0]["value"].split()[0] in bool_dict:
        print(f"Invalid boolean value: {childSentence[0]['value']}")
        return False
    for i in range(1, len(childSentence)):
        if childSentence[0]:
            if not valid_command(childSentence[i]):
                return False
    return True


def repeat_comm(sentence: list, childSentence: list) -> bool:

    if len(childSentence) != 1 or len(sentence) != 2:
        print("More parameters than expected for the repeat function.")
        return False
    return valid_numeric_value(sentence[1]) and valid_command(childSentence[0])


# TODO Make the function so it creates the function.
def defun_comm(sentence: list, childSentence: list) -> bool:

    if len(sentence) != 2 and len(childSentence) < 2:
        print("Invalid syntax for function creation.")
        return
    return createFunction(sentence[1], childSentence[0]["value"].split())


def defun_p_foo(defun: bool, defun_parameters: list, local_parameters: dict) -> None:
    """
    This function populates a dictionary with all the local parameters that should
    be accessible inside of a function declaration.
    """
    if defun and not local_parameters:
        for parameter in defun_parameters:
            local_parameters[parameter] = -1
    elif not defun:
        local_parameters = []


def loop_comm(sentence: list, childSentence: list) -> bool:
    if len(sentence) != 1:
        print(
            f"Invalid syntax for the 'loop' command: '{' '.join(sentence)}'. The 'if' conditional and the command must be inside parenthesis."
        )
        return False
    if (
        childSentence[0]["value"].split()[0] != "if"
        or len(childSentence[0]["value"].split()) != 1
    ):
        print(
            f"Invalid parameter for the 'loop' command: '{childSentence[0]['value']}'. "
            f"Must be followed by an 'if' conditional."
        )
        return False
    elif not valid_command(childSentence[1]):
        print(f"Invalid command: '{childSentence[1]['value']}'")
        return False
    return True


control_dict = {
    "if": if_comm,
    "repeat": repeat_comm,
    "defun": defun_comm,
    "loop": loop_comm,
}


# TODO add declared functions recognition
def lexer(sentence: list, children: list, defun: bool, defun_parameters: list) -> bool:
    """The lexer determines whether a sentence's 'token' (the first instruction)
    is either a command, a control structure or a function call.
    It calls the corresponding sub-lexer function.
    """
    defun_p_foo(defun, defun_parameters, local_parameters)

    try:
        token = sentence[0]
    except:
        token = None
    if token in commands_dict:
        return command_lexer(token, sentence)
    elif token in bool_dict:
        return bool_lexer(token, sentence, children)
    elif token in control_dict:
        return control_lexer(token, sentence, children)
    elif token == "raiz":
        return True
    elif token in functionDefinitions:
        if len(sentence) - 1 == len(functionDefinitions[token]):
            return True
        else:
            print(
                f"The {token} function requires {len(functionDefinitions[token])} parameters. {len(sentence)-1} were provided"
            )
    elif defun:
        """print("Entered defun")
        print(sentence, local_parameters)"""
        if not token and not local_parameters:
            return True
        else:
            for parameter in sentence:
                if parameter not in local_parameters:
                    print(
                        f"The variable {'parameter'} is not a valid variable or function parameter."
                    )
                    return False
            return True
    elif not token:
        if children:
            return True
    print(f"Invalid syntax: '{' '.join(sentence)}'")
    return False


def command_lexer(token: str, sentence: list) -> bool:
    return commands_dict[token](sentence)


def bool_lexer(token: str, sentence: list, childSentence=[]) -> bool:

    if childSentence:
        return bool_dict[token](sentence, childSentence)
    else:
        return bool_dict[token](sentence)


def control_lexer(token: str, sentence: list, childSentence=[]) -> bool:
    if childSentence:
        return control_dict[token](sentence, childSentence)
    else:
        return control_dict[token](sentence)
