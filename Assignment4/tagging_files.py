import nltk

files = ['formal', 'informal']

for file_name in files:
    with open(f'{file_name}_cleaned.txt', 'r') as file:
        with open(f'{file_name}_tagged.txt', 'w') as output:
            lines = list(file)

            for line in lines:
                line = line.strip().split()

                tagged_line = nltk.pos_tag(line)
                for word, pos in tagged_line:
                    output.write(f"{word} ({pos}) ")
                output.write("\n")