with open('yelp_AZ_2021.json', 'r') as file, open('updated_yelp_AZ_2021.json', 'w') as outfile:
    outfile.write('{ "data": [\n')
    lines = list(file)
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        updated_line = f'{lines[i]},\n' if i < len(lines) - 1 else f'{lines[i]}\n'
        outfile.write(updated_line)
    outfile.write(']\n}')
