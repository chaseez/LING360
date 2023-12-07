from string import punctuation

with open('all_cleaned_text.txt') as file:
    unique_chars = set()
    lines = list(file)

    for line in lines:
        cleaned_line = line.strip()

        for c in cleaned_line:
            unique_chars.update(c)

    print(len(unique_chars))

with open('char_set.txt', 'w') as outfile:
    for char in unique_chars:
        outfile.write(f'{char}\n')
