import re
import string

files = ['formal', 'informal']

for file_name in files:
    with open(f'{file_name}.txt', 'r') as file:
        with open(f'{file_name}_cleaned.txt', 'w') as output:
            lines = list(file)

            for line in lines:
                line = line.strip().split()

                new_words = []
                for word in line:
                    word = re.sub(r'[“”",?()*%]','', word)
                    word = re.sub(r'-',' ', word)
                    word = re.sub(r'\.\s+', '\n', word)
                    new_words.append(word)

                output.write(" ".join(new_words))
                output.write("\n")
