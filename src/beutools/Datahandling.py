import os


#FIXME
def createPath(relPath: str) -> str:
    scriptDir = os.path.dirname(__file__)
    return os.path.join(scriptDir, relPath)


def createSavePath(fileName: str) -> str:
    return createPath('../res/out/' + fileName)


def createSavePath(fileName: str) -> str:
    return createPath('../res/out/' + fileName)


def createGUIPath(fileName: str) -> str:
    return createPath('../res/out/' + fileName)


def createReadPath(fileName: str) -> str:
    return createPath('../res/dat/' + fileName)


def createSaveFile(fileName: str) -> None:
    file = open(createSavePath(fileName), 'w+')
    file.close()
    return


def addToSaveFile(fileName: str, line: str) -> None:
    file = open(createSavePath(fileName), 'a')
    file.write(line)
    file.close()
