import string

total_nominalised_words = 0

with open('input.txt', 'r') as file:
    lines = list(file)

    # Cleaning the data from extra characters
    symbols_to_remove = string.punctuation

    cleaned_lines = []
    for line in lines:
        line = line.strip().split()

        cleaned_line = []
        for word in line:
            cleaned_word = ""
            for char in word:
                if char == '.':
                    cleaned_word += '\n'
                    continue
                if char == '-' or char == '/':
                    cleaned_word += ' '
                    continue
                if char in symbols_to_remove or char == '“' or char == '”' or char == '’':
                    continue
                cleaned_word += char

            cleaned_line.append(cleaned_word)

        cleaned_lines.append(" ".join(cleaned_line))

    with open('cleaned_input.txt', 'w') as o_file:
        for line in cleaned_lines:
            o_file.write(line)
            o_file.write("\n")
