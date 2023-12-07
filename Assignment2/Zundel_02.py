import re

with open('cleaned_corpus.txt', 'r') as file:
    lines = list(file)

    # Keeping track of words that match the nominalized pattern
    total_nominalized = []
    for line in lines:
        """
        Find words that end with -ing, -or, -er, -ee, -tion,
        -sion, -ment, -ence, -ance
        """
        line = line.lower()
        total_nominalized += re.findall(r'\w{4,}(?:ing|or|er|ee|tion|'
                                        r'sion|ment|ence|ance)s?\b', line)

# Hard coded counts and nominalized words
actual_counts = [3, 1, 4, 1, 1, 3, 1, 2, 1, 1]
actual_words = ['reading', 'successor', 'information', 'learning', 'identification', 'development', 'remediation', 'acquisition', 'instruction', 'understandings']

actual_count = sum(actual_counts)

# Checking for false positives
false_positives = []

for word in total_nominalized:
    if word not in actual_words:
        false_positives.append(word)

# Checking for words not caught by the re.findall()
missing_words = 0
for word in actual_words:
    if word not in total_nominalized:
        missing_words += 1

# How many of the actual words were found
precision = (actual_count - missing_words) / actual_count

# How many false positives were found
recall = (len(total_nominalized) - len(false_positives)) / len(total_nominalized)

print(precision, recall)