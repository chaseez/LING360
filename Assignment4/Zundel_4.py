import re

files = ['formal', 'informal']

for filename in files:
    with open(f"{filename}_cleaned.txt", "r") as file:
        lines = list(file)

        contractions = []
        for line in lines:
            line = line.strip().split()

            for word in line:
                if re.match(r"\w+'\w+$", word):
                    contractions.append(word)


    with open(f"{filename}_tagged.txt", "r") as file:
        lines = list(file)

        pronouns = []
        modal_verbs = []
        for line in lines:
            line = line.strip().split()

            for word in line:
                if re.match(r"\(PRP\)", word):
                    pronouns.append(word)
                if re.match(r"\(MD\)", word):
                    modal_verbs.append(word)

        print(contractions, pronouns, modal_verbs)
