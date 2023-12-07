from nltk.corpus import wordnet as wn
import re


def pluralize(word):

    # If the word ends in "us"
    # Remove the "us" and add an "i"
    if re.match('\w+us$', word):
        # return word[:len(word)-2] + 'i'
        return re.sub('us$', 'i', word)

    # If the word ends in "is"
    # Remove the "is" and add an "es"
    if re.match('\w+is$', word):
        return re.sub('is$', 'es', word)

    # If the word ends with an "s", "s", "ss", "sh", "ch", "x", or "z"
    # Add an "es"
    if re.match('\w+[sc]?[oshxz]$', word):
        return word + 'es'

    # If the word ends in "y"
    # Remove the "y" and add an "ies"
    if re.match('\w+[aeiou]y$', word):
        return word + 's'

    # If the word ends in "y"
    # Remove the "y" and add an "ies"
    if word[-1] == 'y':
        return re.sub('y$', 'ies', word)

    # If the word ends in "on"
    # Remove the "on" and add an "a"
    if re.match('\w+on$', word):
        return re.sub('on$', 'a', word)

    # Add an "s" to the end of the word if it
    # doesn't match any other pattern
    return word + "s"


def depluralize(word):
    # If the word end in 'ies'
    # Remove the 'ies' and add a 'y' to the end
    if re.match('\w+ies$', word):
        return re.sub('ies$', 'y', word)

    # If the word ends in an "es",
    # Remove the last two letters
    if re.match('\w+es$',word):
        return re.sub('es$', '', word)

    # If the word ends in an "a"
    # Replace the "a" with "on"
    if re.match('\w+a$', word):
        return re.sub('a$', 'on', word)

    # If the word ends in "i"
    # Replace the "i" with "us"
    if re.match('\w+i$', word):
        return re.sub('i$', 'us', word)

    # Remove the last letter if it
    # doesn't match any other pattern
    else: return re.sub('s$', '', word)


with open('wordbank.txt', 'r') as file:
    words = list(file)

    # Removing the \n's from the file
    cleaned_words = []
    for word in words:
        cleaned_words.append(word.strip())

    # Pairing up the word with the associated meanings
    word_pairs = {}
    for word in cleaned_words:
        word_pairs[word] = wn.synsets(word)

    # Checking for the noun (.n.) tag in the meaning
    nouns = []
    for word, meanings in word_pairs.items():
        # print(word, meaning)
        for meaning in meanings:
            if re.match("\w*\.n\.\w*", meaning.name()):
                nouns.append(word)
                break
            # print(meaning.name())

    # Testing out my pluralization and de-pluralization functions
    for noun in nouns:
        print('\nHere\'s the plural form')
        noun = pluralize(noun)
        print(noun)
        print('Here\'s the singular form')
        print(depluralize(noun))


while True:
    word = input('Type in any word and I\'ll pluralize it and possible de-pluralize it too\n')
    word = pluralize(word)
    print(f'Here\'s the plural form: {word}')
    print(f'Here\'s the singular form: {depluralize(word)}')
    word = input('Do you want to do another word? (y)es or (n)o: ')

    if 'n' in word:
        break