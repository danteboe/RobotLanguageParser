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
        .replace(": ", ":")
        .replace(" :", ":")
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
        if c=='(':
            l_parenthesis+=1
        elif c==')':
            l_parenthesis-=1
        if l_parenthesis<0:
            print("Invalid syntax: closing parentheis ')' does not have respective opening parentheis '('")
            return False
        
    if l_parenthesis>0:
        print('Invalid syntax: Unclosed parenthesis.')
        return False
    elif l_parenthesis==0:
        return True

#print(parenthesisRight("()"))

def runCode(tree) -> None:
    # dfs from left to right, emulate code running
    # any var creation, change of definition must go through to emulator.py to the supported functions

    pass


def init() -> None:
    src = readCode()
    src = cleanCode(src)

    if not parenthesisRight(src):
        return

    tree = createTree(src)

    print("-" * 60 + " TEXT " + "-" * 60)
    print(src)

    print("-" * 60 + " TREE " + "-" * 60)
    print(tree)


init()

print("Code's syntaxis is wrong")
