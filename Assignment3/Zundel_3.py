import re

with open('cleaned_input.txt', 'r') as file:
    lines = list(file)

    """
    regex_patterns contents
    ------------------------
    [0]: matches words that contain 'hat'
    [1]: matches words that start with two letters and ends with those two letters flipped
    [2]: matches words that have two repeating vowels
    [3]: matches words that start with two consonants
    [4]: matches words that have two repeating consonants
    """

    regex_patterns = [r'^\w*hat\w*$',
                      r'^(\w)(\w)\w+\2\1$',
                      r'^\w+([aeiou])\1\w*$',
                      r'^[bcdfghjklmnpqrstvwxyz]{2}\w+$',
                      r'^\w+([bcdfghjklmnpqrstvwxyz])\1\w*$']

    pattern_words = {}

    for line in lines:
        # make all words lowercase and get rid of excess whitespace
        line = line.strip().lower().split()

        for word in line:

            # loop through each regular expression pattern for each word
            for pattern in regex_patterns:
                if re.match(pattern, word):
                    # Creating group within the dictionary to hold all the matching words with the corresponding regex
                    if pattern not in pattern_words:
                        pattern_words[pattern] = []
                    pattern_words[pattern].append(word)

    for key, value in pattern_words.items():
        print(f"Here's the regex: {key}\nIt matched {len(value)} words!\nHere are the words: {value}\n")
