from Zundel_5 import process_file

with open('./Mini-CORE_new/1+HI+HT+HI-HI-HI-HI+FH-HT-HT-HT+NNNN+0142743.txt', 'r', encoding='cp437') as file:
    single_file = {}

    lines = list(file)

    process_file(lines, single_file)

    print(single_file)