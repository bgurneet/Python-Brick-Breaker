import re
import time
import datetime

file = open("EnglishWords.txt", 'r')
#storing each line in the file as a separate element in a list
dictWords = file.readlines()
#getting rid of the '\n' in each element by getting rid of the last two characters
#also get rid of all the leading and trailing whitespaces in each line of the file (in case there are any)
dictWords = [word[:len(word)-1].strip() for word in dictWords]

def getTextFromFile(filename):
    content = ""
    try:
        #using a try-except block here just in case the user enters a filename that doesn't exist
        file = open(filename, 'r')
        content = file.read()
    except:
        #file was not found
        print("ERROR: File not found!")
    #return the content of the file in lowercase
    return content.lower()

def processInput(sentence, filename):
    sentence = sentence.strip()
    #re pattern is used to recognise anything that is not a digit or a letter (alphanumeric)
    rePattern = "[^'\-a-zA-Z]+"
    #replace every non alphanumeric character in the string with a whitespace
    sentence = re.sub(rePattern, ' ', sentence)
    #getting the words in the input by splitting the input string by occurences of the whitespace character
    sentenceWords = sentence.split(" ")
    #get rid of all the empty string literals from the list
    sentenceWords = list(filter(lambda x: x != '', sentenceWords))
    sentenceWords = list(map(lambda x: x.replace("'", "") if "'" in x else x, sentenceWords))
    sentenceWords = list(map(lambda x: x.replace("-", "") if "-" in x else x, sentenceWords))
    #the number of correctly spelt words in incremented every time we encounter such a word in the input
    correctWords = 0
    totalWords = len(sentenceWords)
    for (index, word) in enumerate(sentenceWords):
        #iterating over every word in the input
        #let the user know if it is spelled correctly ot not 
        if word in dictWords:
            correctWords += 1
        else:
            sentenceWords[index] = "?"+word+"?"

    incorrectWords = totalWords - correctWords
    print("Number of words:", totalWords)
    print("Number of correctly spelt words:", correctWords)
    print("Number of incorrectly spelt words:", incorrectWords)
    #make the output file with sentenceWords
    outputString = ' '.join(sentenceWords)
    file = open("out_"+filename, 'w')
    date = datetime.date.today().strftime("%d-%m-%Y")
    time = datetime.datetime.now().time().strftime("%H:%M")
    file.write(date + " " + time + "\n")
    file.write("Number of words: "+str(totalWords)+"\n")
    file.write("Number of correctly spelt words: "+str(correctWords)+"\n")
    file.write("Number of incorrectly spelt words: "+str(incorrectWords)+"\n\n")
    file.write(outputString)



while True:
    sentence = ""
    #if user chooses to input without file, then default filename is set to this
    filename = "shellInput.txt"
    print("\n  S P E L L   C H E C K E R  \n")
    print("1. Check a file")
    print("2. Check a sentence\n")
    print("0. Quit\n")
    choice = input("Enter choice: ")
    print()
    startTime = time.time()
    if choice == "1":
        #filename is changed if they choose to provide the input from a file
        filename = input("Enter the name of the file to spellcheck: ")
        sentence = getTextFromFile(filename)
        if sentence == "":
            #there was an error in reading the file
            #try getting the input from the user again
            continue
    elif choice == "2":
        #get input from shell
        sentence = input("Enter sentence to spellcheck: ").lower()
    elif choice == "0":
        #user chose to exit so break from loop
        break
    else:
        #choice was not defined to display menu again
        print("ERROR: Invalid Choice!")
        continue
    processInput(sentence, filename)
    endTime = time.time()
    print("\n Time elapsed", (endTime - startTime), "microseconds\n")
    choice = input("Press q [enter] to quit or any other key [enter] to go again: ")
    if choice == 'q':
        break
