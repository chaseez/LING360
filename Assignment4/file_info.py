import glob

files = ['formal.txt', 'informal.txt', 'formal_cleaned.txt', 'informal_cleaned.txt']

for file_name in files:
    with open(f'{file_name}', 'r') as file:
        lines = list(file)

        word_count = 0
        for line in lines:
            line = line.strip().split()
            word_count += len(line)

        print(file_name, word_count)

