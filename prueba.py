import emulator

def checkSintax(regExpression: str, childExp: list) -> bool:
    sentence = regExpression.strip().split()
    cSentences = []
    if childExp:
        for child in childExp:
            childSentence = child["value"].strip().split()
            cSentences.append(childSentence)
    return emulator.lexer(sentence, cSentences)
    
sentence = ' (if (not (blocked?))((move 1)(goend))(null)))'
print(sentence.strip().split())
valid = checkSintax(sentence)
print(valid)
