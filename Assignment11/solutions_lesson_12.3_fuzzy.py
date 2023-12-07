"""
Possible solutions to the in-class practice exercises for
Lesson 12.2
about fuzzy string matching
"""

from thefuzz import fuzz
### Take a couple minutes to run the example code for each of the following four functions and, importantly, understand and explain to a neighbor what each function does: ratio(), partial_ratio(), token_sort_ratio(), token_set_ratio().

# fuzz.ratio()
str1 = "this is a test"
str2 = "this is a test!"
print(fuzz.ratio(str1, str2))
# Output = 97 (these two strings are 97% the same)

# fuzz.partial_ratio()
str1 = "this is a test"
str2 = "this is a test!"
print(fuzz.partial_ratio(str1, str2))
# Output = 100 (the shorter string is a substring of the longer one)

# fuzz.token_sort_ratio()
str1 = "fuzzy wuzzy was a bear"
str2 = "wuzzy fuzzy was a bear"
print(fuzz.ratio(str1, str2))  # Output = 91 (91% the same w/o sorting)
print(fuzz.token_sort_ratio(str1, str2))  # Output = 100 (100% the same after sorting words)

# fuzz.token_set_ratio()
str1 = "fuzzy was a bear"
str2 = "fuzzy fuzzy was a bear"
print(fuzz.token_sort_ratio(str1, str2))  # Output = 84 (84% the same even after sorting)
print(fuzz.token_set_ratio(str1, str2))  # Output = 100 (100% the same when considering only unique words)

### Take a few minutes to understand what extract() and extractOne() return.

# process.extract()
from thefuzz import process
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
print(process.extract("new york jets", choices, limit=2))

# process.extractOne()
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
print(process.extractOne("cowboys", choices))  # default_scorer is WRatio here: https://github.com/seatgeek/thefuzz/blob/master/thefuzz/fuzz.py#LC224
print(process.extractOne("cowboys", choices, scorer=fuzz.token_set_ratio))  # you can pass in a specific scorer if desired


### Formative quiz

# Discuss what the four functions would return for the following pairs of two strings, and then check your guess by using the four functions:
string1 = "Linguistics is the study of language."
string2 = "Linguistics is the study of language!"
print(fuzz.ratio(string1, string2))  # Output = 97
print(fuzz.partial_ratio(string1, string2))  # Output = 97
print(fuzz.token_sort_ratio(string1, string2))  # Output = 100
print(fuzz.token_set_ratio(string1, string2))  # Output = 100

string1 = "Computers are awesome, like, sweet"
string2 = "Computers are awesome, like, sweet sweet"
print(fuzz.ratio(string1, string2))  # Output = 92
print(fuzz.partial_ratio(string1, string2))  # Output = 100
print(fuzz.token_sort_ratio(string1, string2))  # Output = 91
print(fuzz.token_set_ratio(string1, string2))  # Output = 100

string1 = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
string2 = "z y x w v u t s r q p o n m l k j i h g f e d c b a"
print(fuzz.ratio(string1, string2))  # Output = 49
print(fuzz.partial_ratio(string1, string2))  # Output = 49
print(fuzz.token_sort_ratio(string1, string2))  # Output = 100
print(fuzz.token_set_ratio(string1, string2))  # Output = 100

string1 = "abcdefghijklmnopqrstuvwxyz"
string2 = "zyxwvutsrqponmlkjihgfedcba"
print(fuzz.ratio(string1, string2))  # Output = 4
print(fuzz.partial_ratio(string1, string2))  # Output = 4
print(fuzz.token_sort_ratio(string1, string2))  # Output = 4
print(fuzz.token_set_ratio(string1, string2))  # Output = 4
