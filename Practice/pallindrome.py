import math

def pall(word):
    last_index = len(word) - 1

    sub_word = ''
    for  i in range(last_index, -1, -1):
        sub_word+=word[i]

    return sub_word == word



print(pall('racecar'))

