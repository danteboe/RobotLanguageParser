import emulator

def readCode() -> str:
    file_path = "code.txt"

    try:
        with open(file_path, "r") as file:
            code = file.read()

            return code

    except FileNotFoundError:
        print("Error: File not found")

    except Exception as e:
        print("Error reading file: " + e)

    exit()


def cleanCode(src: str) -> str:
    newSrc = (
        " ".join(src.split())
        .replace("( ", "(")
        .replace(" )", ")")
        .replace(") (", ")(")
        .lower()
    )
    return newSrc


def createTree(src: str) -> dict:
    stack = []
    tree = {"value": "raiz", "children": []}
    current_node = tree

    for character in src:
        if character == "(":
            node = {"value": "", "children": []}
            current_node["children"].append(node)
            stack.append(current_node)
            current_node = node

        elif character == ")":
            current_node = stack.pop()

        else:
            current_node["value"] += character

    return tree


def parenthesisRight(src: str) -> bool:
    l_parenthesis = 0
    for c in src:
        if c == "(":
            l_parenthesis += 1
        elif c == ")":
            l_parenthesis -= 1
        if l_parenthesis < 0:
            print(
                "Invalid syntax: closing parentheis ')' does not have respective opening parentheis '('"
            )
            return False

    if l_parenthesis > 0:
        print("Invalid syntax: Unclosed parenthesis.")
        return False
    elif l_parenthesis == 0:
        return True

#Defun checks if the current value corresponds to the "defun" command. 
#It facilitates its syntactical analysis.
def dfs(tree, depth, defun:bool):
    try:
        token = tree["value"].strip().split()[0]
    except:
        token = None

    if token == "defun":
        defun = True
        defun_parameters = [parameter for parameter in tree["children"][0]["value"].split()]
    else: 
        defun_parameters=[]

    if not checkSintax(tree["value"], tree["children"], defun, defun_parameters):
        print("Code's syntaxis is wrong")
        return 

    if "children" in tree:
        for child in tree["children"]:
            if not dfs(child, depth + 1, defun):
                return False

    return True

def checkSintax(regExpression: str, childExp: list, defun:bool, defun_parameters:list) -> bool:
    sentence = regExpression.strip().split()
    print(regExpression)
    return emulator.lexer(sentence, childExp, defun, defun_parameters)



def init() -> None:
    src = readCode()
    src = cleanCode(src.lower())

    if not parenthesisRight(src):
        return

    tree = createTree(src)

    print("-" * 60 + " TEXT " + "-" * 60)
    print(src)

    print("-" * 60 + " TREE " + "-" * 60)
    print(tree)

    print("-" * 60 + " DFS " + "-" * 60)
    if dfs(tree, 0, False):
        print("-" * 60 + " All Good " + "-" * 60)

    exit()


init()

print("Code's syntaxis is wrong")
