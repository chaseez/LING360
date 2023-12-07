import re
import os
import nltk
import time


def process_file(lines, dictionary):
    for line in lines:
        # Cleaning the lines

        # Removing HTML tags
        line = re.sub(r'<.+>', '', line)
        # Removing extra JSON information
        line = re.sub(r'\{.+\}', '', line)
        # Removing punctuation, so NLTK POS Tagger can recognize word
        line = re.sub(r'[.?\'",\-()$/\\*\^]', ' ', line)

        line = line.strip().split()

        # Create list of words with POS tags
        tagged_line = nltk.pos_tag(line)

        for word, pos in tagged_line:
            # Filtering for Modal Verbs, Personal Pronouns, or Numbers / Cardinal Numbers
            if pos == 'MD' or pos == 'PRP' or pos == 'CD':
                if pos not in dictionary:
                    dictionary[pos] = 0
                dictionary[pos] += 1

            if 'word_count' not in dictionary:
                dictionary['word_count'] = 0
            dictionary['word_count'] += 1


def normalize_data(normalized_dictionary, dictionary):
    # Getting total word count
    word_count = dictionary['word_count']

    # Getting genre name
    genre = dictionary['genre']

    # Using word count as key
    normalized_dictionary[genre] = {}
    for key in dictionary:
        if key != 'word_count' and key != 'genre':
            # Dividing the count of CD, PRP, or MD and dividing by word count
            # Then multiplying by 1000 to get # of words per 1000 words
            normal_calculation = (dictionary[key] / word_count) * 1000

            # Using CD, PRP, or MD as key to hold normalized count per 1000 words
            normalized_dictionary[genre][key] = normal_calculation


def write_to_csv(normalized_dictionary):
    with open('normalized_word_count.csv', 'w') as out_file:
        headers = ['Register', 'MD', 'PRP', 'CD']

        # Writing the headers as the first line
        out_file.write(','.join(headers))
        out_file.write('\n')
        for genre, word_count_dict in normalized_dictionary.items():
            # Casting each word count value to a string for the join function
            md = str(word_count_dict['MD'])
            prp = str(word_count_dict['PRP'])
            cd = str(word_count_dict['CD'])

            line = [genre, md, prp, cd]

            # Writing the genre first, then the modal count, then the personal pronouns, then the cardinal numbers
            # with each word separated by a comma
            out_file.write(','.join(line))
            out_file.write('\n')


if __name__ == '__main__':
    start = time.time()
    # Getting names of all the files in the Mini Core Corpus
    all_files = os.listdir('./Mini-CORE_new')

    # Initializing all the dictionaries
    HI = {'genre': 'HI'}
    ID = {'genre': 'ID'}
    IN = {'genre': 'IN'}
    IP = {'genre': 'IP'}
    LY = {'genre': 'LY'}
    NA = {'genre': 'NA'}
    OP = {'genre': 'OP'}
    SP = {'genre': 'SP'}

    for filename in all_files:
        with open(f'./Mini-CORE_new/{filename}', 'r', encoding='cp437') as file:
            # Getting the genre of the file
            file_type = filename[2:4]

            # Making all the lines into a list
            lines = list(file)

            # Passing the corresponding dictionary
            if file_type == 'HI':
                process_file(lines, HI)
            elif file_type == 'ID':
                process_file(lines, ID)
            elif file_type == 'IN':
                process_file(lines, IN)
            elif file_type == 'IP':
                process_file(lines, IP)
            elif file_type == 'LY':
                process_file(lines, LY)
            elif file_type == 'NA':
                process_file(lines, NA)
            elif file_type == 'OP':
                process_file(lines, OP)
            elif file_type == 'SP':
                process_file(lines, SP)

    # Putting all the dictionaries in a list to loop through
    all_dictionaries = [HI, ID, IN, IP, LY, NA, OP, SP]
    normalized_data = {}

    for dictionary in all_dictionaries:
        normalize_data(normalized_data, dictionary)

    write_to_csv(normalized_data)

    print(start - time.time())
