#TODO make commands not case-sensitive.

grid = []

variableDefinitions = {}
functionDefinitions = {}

#Numeric constants.
constants = {"Dim": -1,
             "myXpos": -1,
             "myYpos": -1,
             "myChips": -1,
             "myBalloons": -1,
             "balloonsHere": -1,
             "ChipsHere": -1,
             "Spaces": -1}

#Direction constants
directions = {":left":-1,
              ":right":-1,
              ":front":-1,
              ":back":-1}

#"Turn" command-specific direction constants
t_directions = {":left":-1,
              ":right":-1,
              ":around":-1}

#Orientation constants
orientations = {":north":-1,
                ":south":-1,
                ":east":-1,
                ":west":-1}

#Prop constants
props = {":balloons":-1,
         ":chips":-1}

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


def createFunction(funcName: str, value: any) -> bool:
    if funcName in functionDefinitions:
        return False

    functionDefinitions[funcName] = value

    return True

def valid_numeric_value(n:str)->bool:
    if n not in constants:
        try:
            n = int(n)
        except:
            try: #checks if n corresponds to a variable that was assigned a numeric value.
                n=int(variableDefinitions[n])
            except:
                print(f"Invalid numeric value: {n}")
                return False
    return True

def valid_t_direction(d:str)->bool:
    var_value = None

    if d not in t_directions:
        try: #Checks if d corresponds to a variable that was assigned a direction constant
            var_value = variableDefinitions[d]
        except:
            print(f"Invalid direction value: '{d}'")
            return False
        if var_value not in t_directions:
            print(f"Invalid direction value: '{d}'")
            return False
    return True

def valid_direction(d:str)->bool:
    var_value = None

    if d not in directions:
        try: #Checks if d corresponds to a variable that was assigned a direction constant
            var_value = variableDefinitions[d]
        except:
            print(f"Invalid direction value: '{d}'")
            return False
        if var_value not in directions:
            print(f"Invalid direction value: '{d}'")
            return False
    return True

def valid_orientation(o:str)->bool:
    var_value = None

    if o not in orientations:
        try: #Checks if o corresponds to a variable that was assigned an orientation constant
            var_value = variableDefinitions[o]
        except:
            print(f"Invalid orientation value: '{o}'")
            return False
        if var_value not in orientations:
            print(f"Invalid orientation value: '{o}'")
            return False
    return True

def valid_prop(p:str)->bool:
    var_value = None

    if p not in props:
        try: #Checks if p corresponds to a variable that was assigned a prop constant
            var_value = variableDefinitions[p]
        except:
            print(f"Invalid prop value: '{p}'")
            return False
        if var_value not in props:
            print(f"Invalid prop value: '{p}'")
            return False
    return True

def defvar_foo(sentence:list)->bool:
    """
    Checks if the sentence follows the syntax for
    defvar name n
    where name is the number of the variable to initialize and 
    n is a number or a constant.
    """

    if len(sentence)!=3:
        print(f"""Invalid variable declaration syntax: {' '.join(sentence)}
Must follow the syntax 'defvar name n'""")
        return False
    
    v_name = sentence[1]
    v_n = sentence[2]
    n= None
    
    if not valid_numeric_value(v_n):
        return False
    else:
        if v_n in constants:
            n = constants[v_n]
        else:
            n = int(v_n)
    return createVariable(v_name, n)
        
def equal_foo(sentence:list)->bool:
    """
    Checks if the sentence follows the syntax for
    = name n
    where name is the number of the variable to modify and 
    n is a number or a constant.
    """
    if len(sentence)!=3:
        print(f"""Invalid variable modification syntax: {' '.join(sentence)}
Must follow the syntax '= name n'""")
        return False
    
    v_name = sentence[1].strip() 
    v_n = sentence[2]
    n= None

    if not valid_numeric_value(v_n):
        return False
    else:
        if v_n in constants:
            n = constants[v_n]
        else:
            n = int(v_n)
    return modifyVariable(v_name, n)
    
def move_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    move n 
    syntax. 
    n must be a numeric value or a constant.
    """
    if len(sentence)!=2:
        print(f"""Invalid 'move' function syntax: {' '.join(sentence)}
Must follow the syntax 'move n'""")
        return False
    
    return valid_numeric_value(sentence[1])

def skip_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    skip n 
    syntax. 
    n must be a numeric value or a constant.
    """
    if len(sentence)!=2:
        print(f"""Invalid 'skip' function syntax: {' '.join(sentence)}
Must follow the syntax 'skip n'""")
        return False
    
    return valid_numeric_value(sentence[1])

#TODO check :front direction
def turn_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    turn D 
    syntax. 
    D must be one of the direction constants specific for the 'turn' function.
    """
    if len(sentence)!=2:
        print(f"""Invalid 'turn' function syntax: {' '.join(sentence)}
Must follow the syntax 'turn D'""")
        return False
    
    return valid_t_direction(sentence[1])
    
def face_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    face O 
    syntax. 
    O must be one of the orientation constants.
    """
    if len(sentence)!=2:
        print(f"""Invalid 'face' function syntax: {' '.join(sentence)}
Must follow the syntax 'face O'""")
        return False
    return valid_orientation(sentence[1])

def put_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    put X n 
    syntax. 
    X must be one of the prop constants.
    n must be a valid numeric value
    """
    if len(sentence)!=3:
        print(f"""Invalid 'put' function syntax: {' '.join(sentence)}
Must follow the syntax 'put X n'""")
        return False
    return (valid_prop(sentence[1]) and valid_numeric_value(sentence[2]))

def pick_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    pick X n 
    syntax. 
    X must be one of the prop constants.
    n must be a valid numeric value
    """
    if len(sentence)!=3:
        print(f"""Invalid 'pick' function syntax: {' '.join(sentence)}
Must follow the syntax 'pick X n'""")
        return False
    return (valid_prop(sentence[1]) and valid_numeric_value(sentence[2]))

def move_dir_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    move-dir n D 
    syntax. 
    n must be a valid numeric value
    D must be one of the direction constants.
    """
    if len(sentence)!=3:
        print(f"""Invalid 'move-dir' function syntax: {' '.join(sentence)}
Must follow the syntax 'move-dir n D'""")
        return False
    n= sentence[1]
    d= sentence[2]
    return (valid_numeric_value(n) and valid_direction(d))

def run_dirs_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    run-dirs Ds
    syntax. 
    Ds is a non-empty list of directions.
    """
    if len(sentence)<=1:
        print(f"""Invalid 'run-dirs' function syntax: {' '.join(sentence)}
Must give a non-empty list of directions.'""")
        return False
    
    for d in sentence[1:]:
        if not valid_direction(d):
            return False
    return True

def move_face_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    move-face n O 
    syntax. 
    n must be a valid numeric value
    O must be one of the orientation constants.
    """
    if len(sentence)!=3:
        print(f"""Invalid 'move-face' function syntax: {' '.join(sentence)}
Must follow the syntax 'move-face n O'""")
        return False
    
    n= sentence[1]
    o= sentence[2]

    return (valid_numeric_value(n) and valid_orientation(o))

def null_foo(sentence:list)->bool:
    """
    Verifies whether a sentence follows a valid
    null syntax. 
    null must not have any arguments.
    """
    if len(sentence)!=1:
        print(f"""Invalid 'null' function syntax: {' '.join(sentence)}
The 'null' function must not have any arguments.""")
        return False
    return True

commands_dict = {
    'defvar': defvar_foo,
    '=': equal_foo,
    'move': move_foo,
    'skip': skip_foo,
    'turn': turn_foo,
    'face': face_foo,
    'put': put_foo,
    'pick': pick_foo,
    'move-dir': move_dir_foo,
    'run-dirs': run_dirs_foo,
    'move-face': move_face_foo,
    'null': null_foo
}

def lexer(sentence:list)->bool:
    """The lexer determines whether a sentence's 'token' (the first instruction)
        is either a command, a control structure or a function call.
        It calls the corresponding sub-lexer function.
    """
    token = sentence[0]
    if token in commands_dict:
        return command_lexer(token, sentence)

def command_lexer(token:str, sentence:list)->bool:
    return commands_dict[token](sentence)
