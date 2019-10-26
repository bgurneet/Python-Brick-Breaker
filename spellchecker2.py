import re #import the regular expressions library
file = open("EnglishWords.txt", 'r')
#storing each line in the file as a separate element in a list
dictWords = file.readlines()
#getting rid of the '\n' in each element by getting rid of the last two characters
#also get rid of all the leading and trailing whitespaces in each line of the file (in case there are any)
dictWords = [word[:len(word)-1].strip() for word in dictWords]

while True:
    #get input and convert it to lowercase
    sentence = input("Enter sentence to spellcheck: ").lower()
    #get rid of all leading and trailing whitespaces
    sentence = sentence.strip()
    #re pattern is used to recognise anything that is not a digit or a letter (alphanumeric)
    rePattern = '[^0-9a-zA-Z]+'
    #replace every non alphanumeric character in the string with a whitespace
    sentence = re.sub(rePattern, ' ', sentence)
    #getting the words in the input by splitting the input string by occurences of the whitespace character
    sentenceWords = sentence.split(" ")
    #get rid of all the empty string literals from the list
    sentenceWords = list(filter(lambda x: x != '', sentenceWords))

    #the number of correctly spelt words in incremented every time we encounter such a word in the input
    correctWords = 0
    totalWords = len(sentenceWords)
    for word in sentenceWords:
        #iterating over every word in the input
        #let the user know if it is spelled correctly ot not 
        if word in dictWords:
            correctWords += 1
            print(word + " spelt correctly")
        else:
            print(word + " not found in dictionary")

    incorrectWords = totalWords - correctWords
    print("Number of words:", totalWords)
    print("Number of correctly spelt words:", correctWords)
    print("Number of incorrectly spelt words:", incorrectWords)
    choice = input("Press q [enter] to quit or any other key to go again: ")
    if choice == 'q':
        #exit loop
        break
    #if choice is not 'q' it just continues anyway so we don't need to specify anything
