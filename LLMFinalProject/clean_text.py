from string import punctuation
from time import time
import os, re


def clean_line(line):
    remove_escape_char_english = re.sub(pattern=r'(\w+)&#?[A-Za-z0-9]+;?|&#?[a-zA-Z0-9]+;',
                                        repl='',
                                        string=line)

    remove_parenthesis_english = re.sub(pattern=r'(\(|\[).+(\)|\])',
                                        repl='',
                                        string=remove_escape_char_english)

    remove_extra_brackets_english = re.sub(pattern=r'[({\[)}\]]',
                                           repl='',
                                           string=remove_parenthesis_english)

    remove_xml_tags_english = re.sub(pattern=r'(<|〈|〈)[^>〉〉]+(>|〉|〉)',
                                     repl='',
                                     string=remove_extra_brackets_english)

    remove_excess_angles_english = re.sub(pattern=r'(<|>)',
                                          repl='',
                                          string=remove_xml_tags_english)

    remove_nbsp_english = re.sub(pattern=r'\U000000a0',
                                 repl='',
                                 string=remove_excess_angles_english)

    remove_ampersand_english = re.sub(pattern=r'&\w+',
                                      repl='',
                                      string=remove_nbsp_english)

    remove_https_english = re.sub(pattern=r'https?://\w+\.(\w+|\w+\.|\w/)*',
                                  repl='',
                                  string=remove_ampersand_english)

    normalize_whitespace_english = re.sub(pattern=r'\s+',
                                          repl=' ',
                                          string=remove_https_english)
    # “ ”

    normalize_double_quotes_english = re.sub(pattern=r'(“|”)',
                                             repl='"',
                                             string=normalize_whitespace_english)

    # ‘’

    normalize_single_quotes_english = re.sub(pattern=r'(‘|’)',
                                             repl='\'',
                                             string=normalize_double_quotes_english)

    remove_equals_english = re.sub(pattern=r'=+',
                                   repl='',
                                   string=normalize_single_quotes_english)

    remove_at_symbol_english = re.sub(pattern=r'@+\d*\b',
                                      repl='',
                                      string=remove_equals_english)

    remove_pos_tags_english = re.sub(pattern=r'((\w*)_(\w*)|(\W*)_(\W*))\s',
                                     repl=r'\2\4 ',
                                     string=remove_at_symbol_english)

    remove_non_word_chars = re.sub(pattern=r'$[^\w\-]+^',
                                   repl=r'',
                                   string=remove_pos_tags_english)

    remove_extra_symbols = re.sub(pattern=r'(\'|\"|\`|\~|\+|\;|\_)',
                                  repl=r'',
                                  string=remove_non_word_chars)

    return remove_extra_symbols


def get_text_and_words_from_file(lines):
    words = set()
    text = ''
    for line in lines:
        line = clean_line(line)
        if len(line.split()) > 0:
            text += line.lower()
            words.update(line.strip().lower().split())
    return text, words


def get_text_and_words_from_vrt(lines):
    text = ''
    words = set()
    for line in lines:
        line = clean_line(line)
        w = line.lower().split()
        if len(w) > 0:
            if w[0] in punctuation:
                text = text[:-1]

            text += w[0] + ' '
            if w[0] not in punctuation:
                words.add(w[0])
    return text, words


if __name__ == '__main__':
    start_time = time()
    count = 0
    all_words = set()
    cleaned_text_path = 'all_cleaned_text.txt'
    with open(cleaned_text_path, 'w') as outfile:

        for root, dir, files in os.walk('Corpora'):
            count += 1

            if count == 1:  # Only want to get the files within each directory
                continue

            for filename in files:
                if filename.endswith('.zip'):
                    print('.zip file')
                    continue

                try:
                    with open(f'{root}/{filename}', 'r') as infile:
                        lines = list(infile)
                    if filename.endswith('.vrt'):
                        text, words = get_text_and_words_from_vrt(lines)
                    else:
                        text, words = get_text_and_words_from_file(lines)
                    # print(f'{filename}')
                    # print(text)
                    # print(words)
                    all_words.update(words)
                    outfile.write(text + '\n')



                except UnicodeDecodeError:
                    print('Wrong encoding')
                    try:
                        with open(f'{root}/{filename}', 'r', encoding='cp437') as infile:
                            lines = list(infile)
                        if filename.endswith('.vrt'):
                            text, words = get_text_and_words_from_vrt(lines)
                        else:
                            text, words = get_text_and_words_from_file(lines)
                        # print(f'{filename}')
                        # print(text)
                        # print(words)
                        all_words.update(words)
                        outfile.write(text + '\n')

                    except:
                        print('Another failed encoding')

    print(f'Total runtime: {time()-start_time:.4f}')