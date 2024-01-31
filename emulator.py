grid = []

variableDefinitions = {}
functionDefinitions = {}


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
