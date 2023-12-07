import nltk
import re
import os


def find_noun_bigram_count(lines, register, register_info):
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
                if noun_bigram not in register_info[register]:
                    register_info[register][noun_bigram] = 0

                # Increment noun_bigram count by one
                register_info[register][noun_bigram] += 1


def sort_counts(dictionary):
    # Creating a dictionary to map each register with the sorted values
    counts = {}
    for register, values in dictionary.items():
        # Getting a list of tuples like (noun bi-gram, count)
        bigram_count = list(values.items())
        # Sorting word_count by the count from highest to lowest
        bigram_count.sort(key=lambda i: i[1], reverse=True)
        # Storing the sorted counts into the associated register
        counts[register] = bigram_count
    return counts


def sorted_list_to_csv(sorted_list, register):
    with open(f'./{register}_bigram_frequency_list.csv', 'w') as outfile:
        # Writing headers
        headers = ['Noun Bi-gram', 'Count']
        outfile.write(','.join(headers))
        outfile.write('\n')

        # Writing each word with the associated count
        for bigram, count in sorted_list:
            outfile.write(f'{bigram},{count}\n')


if __name__ == "__main__":
    # Initialize dictionary with
    register_info = {
        "JA_HI": {},
        "JA_BI": {},
        "PS_HI": {},
        "PS_BI": {},
        "TB_HI": {},
        "TB_BI": {}
    }

    # Getting all the files in the AWE directory
    files = os.listdir('./AWE_untagd')

    # Loop through all the .txt files in the current directory
    for curr_file in files:
        with open(f'./AWE_untagd/{curr_file}', 'r', encoding='cp437') as in_file:
            # Getting the register genre (the letters at the indexes 2 and 3)
            register = curr_file[:5]
            lines = list(in_file)

            # Stores all the bi-gram information from each file into register_info
            find_noun_bigram_count(lines, register, register_info)

    # Get a dictionary of sorted bi-gram counts associated with each register
    sorted_counts = sort_counts(register_info)

    # Writing each register's sorted list to a csv
    for register, counts in sorted_counts.items():
        sorted_list_to_csv(counts, register)
