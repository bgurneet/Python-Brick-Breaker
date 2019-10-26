file = open("EnglishWords.txt", 'r')
#storing each line in the file as a separate element in a list
dictWords = file.readlines()
#getting rid of the '\n' in each element by getting rid of the last two characters
#also get rid of all the leading and trailing whitespaces in each line of the file (in case there are any)
dictWords = [word[:len(word)-1].strip() for word in dictWords]

sentence = input("Enter sentence to spellcheck: ")
#get rid of all leading and trailing whitespaces
sentence = sentence.strip()
#getting the words in the input by splitting the input string by occurences of the whitespace character
sentenceWords = sentence.split(" ")

for word in sentenceWords:
    #iterate over each word in the sentenceWords list (which is from the input)
    #let the user know if it is spelled correctly ot not 
    if word in dictWords:
        print(word+" spelt correctly")
    else:
        print(word+" not found in dictionary")
