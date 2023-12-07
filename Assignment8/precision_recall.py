import re

import nltk

register_info = {}

with open(f'./AWE_untagd/JA_BI_01.txt', 'r', encoding='cp437') as in_file:
    # Getting the register genre (the letters at the indexes 2 and 3)
    lines = list(in_file)
    for line in lines:
        # Cleaning HTML Tags
        line = re.sub(r'<.+>', '', line)
        # Replacing any extra punctuation with a space
        line = re.sub(r'[\[\]\\",!?\(\)%\|\-:/┤+]', '', line)
        # Replacing a period and apostrophe with nothing
        line = re.sub(r'[.\']', '', line)
        # Replacing any numbers with a space
        line = re.sub(r'[0-9]+', ' ', line)

        # Removing excess whitespace, making the line lowercase, and generate a list of words
        words = line.strip().lower().split()

        # Tagging all words
        tagged_words = nltk.pos_tag(words)

        # Looping through using i, so I can index into the current and next item to find a bigram
        for i in range(len(tagged_words) - 1):
            # If both the current word and the next word have the "NN" tag
            if tagged_words[i][1] == 'NN' and tagged_words[i + 1][1] == 'NN':
                # Create the noun_bigram key using the noun
                noun_bigram = f'{tagged_words[i][0]} {tagged_words[i + 1][0]}'

                # Initialize count in register_info if not already inside
                if noun_bigram not in register_info:
                    register_info[noun_bigram] = 0

                # Increment noun_bigram count by one
                register_info[noun_bigram] += 1


counts = {}

bigram_count = list(register_info.items())
# Sorting word_count by the count from highest to lowest
bigram_count.sort(key=lambda i: i[1], reverse=True)
# Storing the sorted counts into the associated register
counts["JA"] = bigram_count

for key,value in counts.items():
    for pair in value:
        print(pair)


