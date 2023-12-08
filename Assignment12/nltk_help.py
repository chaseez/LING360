from nltk import pos_tag, word_tokenize

sentence = 'I really don\'t want to know what is going on. Let me seriously try to not figure anything out'

print(pos_tag(word_tokenize(sentence)))
