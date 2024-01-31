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
    return True


def sintaxChecker(tree) -> None:
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

print("Code's sintaxis is wrong")
