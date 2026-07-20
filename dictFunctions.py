import os
import datetime
import re

# GLOBALS
dictCreateTime = ""
dictUpdateTime = ""
currentDict = {}
valid_pos = ( # ordered
    "adjective",
    "adverb",
    "noun",
    "verb"
)

# -----(1)--createDict------------------------------------------------
def createDict(name, path="."):
    global dictCreateTime, dictUpdateTime, dictName, dictPath

    # create the complete path
    completePath = getCompletePath(name, path)

    # create the directories if path is does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # check if the file is already exist
    if os.path.isfile(completePath):
        raise FileExistsError(f"The dictonary {name} is already exist.")

    try:
        # open or create the file
        with open(completePath, "x") as f:
            # get the current date and time
            nowStr = getCurrentTime()
            # assign time to the globals
            dictCreateTime = nowStr
            dictUpdateTime = nowStr
            # write to file
            f.write(nowStr)
            f.write("\n")
            f.write(nowStr)
            # save the complete path variables as global
            dictName = name
            dictPath = path
    except FileExistsError:
        # print message if file is already exist
        raise FileExistsError(f"The dict {name} is already exist.")


# -----(2)--loadDict--------------------------------------------------
def loadDict(name, path="."):
    global dictUpdateTime, dictCreateTime, currentDict

    # clean the current dict
    currentDict = {}

    # get the complete path
    completePath = getCompletePath(name, path)

    # try to open the file
    try:
        f = open(completePath, "r")
    except FileNotFoundError:
        raise FileNotFoundError(f"The dictionary {name} does not exist.")
    except Exception as e:
        raise e

    # get first 2 lines as times
    dictCreateTime = f.readline().rstrip("\n")
    dictUpdateTime = f.readline().rstrip("\n")
    
    for line in f:
        word = line.rstrip("\n")
        plural = f.readline().rstrip("\n")

        PoSDict = {}

        for line in f:
            line = line.rstrip("\n")
            if line == "#":
                break
            pos = line
            definitions = []

            for line in f:
                line = line.rstrip("\n")
                if line == "-":
                    break
                definitions.append(line)

            PoSDict[pos] = definitions

        currentDict[word] = (plural, PoSDict)

    f.close()


# -----(3)--saveDict--------------------------------------------------
def saveDict(name , path="."):
    global dictUpdateTime

    # get compelete path
    completePath = getCompletePath(name, path)

    # create it if it does not exist
    if not os.path.exists(completePath):
        createDict(name, path)

    try: 
        # write current dict to the file
        with open(completePath, "w") as f:
            # write the cration time to the file
            f.write(dictCreateTime + "\n")
            # update the update time and write it to the file
            dictUpdateTime = getCurrentTime()
            f.write(dictUpdateTime + "\n")

            # print the words
            for word in currentDict.keys():
                plural, PoSDict = currentDict[word]
                f.write(word + "\n")
                f.write(plural + "\n")
                for pos in PoSDict:
                    f.write(pos + "\n")
                    for definition in PoSDict[pos]:
                        f.write(definition + "\n")
                    f.write("-" + "\n")
                f.write("#" + "\n")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"The dictionary {name} saved successfully.")


# -----(4)--removeDict------------------------------------------------
def removeDict(name, path="."):
    # create the complete path
    completePath = getCompletePath(name, path)

    # check if it is exist
    if not os.path.exists(completePath):
        raise FileNotFoundError(f"The dictionary {name} does not exist.")

    # try to remove
    try:
        os.remove(completePath)
    except Exception as e:
        raise e


# -----(5)--dictInfo--------------------------------------------------
def dictInfo(name, path=".", showResult=False):
    # create the complete path
    completePath = getCompletePath(name, path)

    try:
        with open(completePath, "r") as file:
            createTime = file.readline().strip()
            updateTime = file.readline().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"The dict {name} does not exist.")
    except Exception as e:
        raise e
    
    
    if(showResult):
        print(f"Created at: {createTime}\n"
                f"Edited at: {updateTime}")
        
    return {
        "Created": createTime,
        "Edited": updateTime
    }


# -----(6)--addWord---------------------------------------------------
def addWord(word, PoS, *definitions, plural="Default"):
    word = word.strip()
    if len(word) <= 0:
        raise ValueError("The word you entered is invalid.")

    # check if there is definition
    if len(definitions) <= 0:
        raise ValueError(f"You must enter at least one definition for the word {word}.")

    # check if the pos which entered is valid
    if not isPosValid(PoS):
        raise ValueError(f"PoS {PoS} is invalid.")

    # convert definitions tuple to the list
    definitions = list(definitions)

    # generate the plural if the plural is deafult
    if(plural=="Default"):
        plural = generatePlural(word)

    underlineExistingWordsInDefinitions(definitions)

    # if the word is not in the dict add it
    if not word in currentDict:
        underlineWordInDefinitions(word)
        currentDict[word] = (plural, {PoS: definitions})

    # update or add new word to the word
    else:
        pluralValue, posDict = currentDict[word]
        if PoS in posDict:
            posDict[PoS].extend(definitions)
        else:
            posDict[PoS] = definitions

        if not plural == None:
            currentDict[word] = (plural, currentDict[word][1])


# -----(7)--removeWord------------------------------------------------
def removeWord(word):
    res = currentDict.pop(word, None)
    if res:
        removeUnderlineWordInDefinitions(word)


# -----(8)--searchWord------------------------------------------------
def searchWord(word, showResult=False):
    value = currentDict.get(word)# if does not exist returns None

    if showResult and value is not None:
        printWord(word)
    
    return value


# -----(9)--listWords-------------------------------------------------
def listWords(showResult=False):
    sortedWords = sorted(currentDict)
    if showResult:
        if len(sortedWords) <= 0:
            print("")
        else:
            for i in range(len(sortedWords)):
                print(f"{i+1}. {sortedWords[i]}")

    return sortedWords


# -----(UTILS)--------------------------------------------------------
def getCompletePath(name, path):
    # we used join for portability
    return os.path.join(path, name + ".dict")

def getCurrentTime():
    # get the current date and time
    now = datetime.datetime.now()
    # convert it to string
    nowStr = now.strftime("%Y-%m-%d %H:%M:%S")
    return nowStr

def printWord(word):
    plural, PoSDict = currentDict[word]
    print(f"\"{word}\" [Plural]: \"{plural}\"\n")

    for pos in valid_pos: # print in pos order
        if pos in PoSDict:
            print (f"{pos}")
            for i in range(len(PoSDict[pos])):
                print(f"{i + 1}. {PoSDict[pos][i]}")

def generatePlural(word):
    if word.lower().endswith(("s", "sh", "ch", "x", "z")):
        return word + "es"

    return word + "s"

def isPosValid(pos):
    for validPos in valid_pos:
        if pos == validPos:
            return True
    
    return False

def underlineIfExist(word, definition):
    pattern = rf"\b{re.escape(word)}\b"

    newDef, count = re.subn(
        pattern,
        lambda match: f"__{match.group(0)}__",
        definition,
        flags=re.IGNORECASE
    )

    if count > 0:
        return (newDef, True)
    else:
        return (newDef, False)

def underlineWordInDefinitions(word):
    for key in currentDict:
        plural, posDict = currentDict[key]
        for pos in posDict:
            definitions = posDict[pos]
            for i in range(len(definitions)):
                newDef, isChanged = underlineIfExist(word, definitions[i])
                if isChanged:
                    definitions[i] = newDef

def underlineExistingWordsInDefinitions(definitions):
    for i in range(len(definitions)):
        for word in currentDict:
            newDef, isChanged = underlineIfExist(word, definitions[i])
            if isChanged:
                definitions[i] = newDef

def removeUnderlineIfExist(word, definition):
    pattern = rf"__(\b{re.escape(word)}\b)__"

    newDef, count = re.subn(
        pattern,
        r"\1",
        definition,
        flags=re.IGNORECASE
    )

    return count > 0, newDef

def removeUnderlineWordInDefinitions(word):
    for key in currentDict:
        plural, posDict = currentDict[key]

        for pos in posDict:
            definitions = posDict[pos]

            for i in range(len(definitions)):
                isChanged, newDef = removeUnderlineIfExist(
                    word,
                    definitions[i]
                )

                if isChanged:
                    definitions[i] = newDef



# -----(TEST FUNCTION(S))---------------------------------------------
def printCurrentDict():
    sortedWords = sorted(currentDict)

    # initilaize the word counter
    wordCounter = 0
    # get the sorted key list by sorted() function
    for word in sortedWords:
        print(f"WORD {wordCounter}")
        printWord(word)
        print("")
        wordCounter += 1