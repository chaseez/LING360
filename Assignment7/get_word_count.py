with open('final_project_proposal.txt') as file:
    lines = list(file)
    total_words = []
    for line in lines:
        total_words.append(len(line.strip().split()))

    print(sum(total_words))