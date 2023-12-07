from math import floor

with open('all_cleaned_text.txt', 'r') as infile:
    lines = list(infile)
    split_idx = floor(len(lines) * 0.8)
    train_split = lines[:split_idx]
    val_split = lines[split_idx:]

    total_lines = 0
    total_words = 0
    with open('train.txt','w') as outfile:
        for line in train_split:
            line = line.strip()
            if len(line) > 0:
                outfile.write(f'{line}\n')
                total_lines += 1
                total_words += len(line.split())

    print(f'train.txt lines: {total_lines}, words: {total_words}')

    total_lines = 0
    total_words = 0
    with open('val.txt','w') as outfile:
        for line in val_split:
            line = line.strip()
            if len(line) > 0:
                outfile.write(f'{line}\n')
                total_lines += 1
                total_words += len(line.split())

    print(f'val.txt lines: {total_lines}, words: {total_words}')