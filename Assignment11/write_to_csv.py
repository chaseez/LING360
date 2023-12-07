
row_headers  = [1,2,3,4]
words = ['alpha', 'omega', 'foobar', 'random']


with open('test.csv', 'w') as file:
    for i in range(len(words)): # [0,1,2,...,len(words)]
        file.write(f'{row_headers[i]},{words[i]}\n')