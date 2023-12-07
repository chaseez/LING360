"""
Solution file for 
Lesson 12.2 document similarity analysis
Most of this code was produced by ChatGPT
"""

# load the workhorses
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

# Change into the directory with the TXT files
os.chdir("../Assignment10")

# Get filenames
filenames = [f for f in os.listdir() if f.lower().endswith("txt")]

# Define an empty list to collect all documents
documents = []

# Loop through the files in the directory
for filename in filenames:

    # Read the file
    with open(filename, mode="r", encoding="utf8") as infile:

        # Tokenize the file content
        tokens = word_tokenize(infile.read())

        # Append the file content as a TaggedDocument to the documents list
        documents.append(TaggedDocument(tokens, [filename]))

# Train the Doc2Vec model
model = Doc2Vec(documents, vector_size=200, window=5, min_count=1, workers=10)

# Get a specific document
with open("../Assignment10/medium.com @robertsevan scraping-dynamically-loaded-content-with-selenium-and-beautifulsoup-2cb7b067.txt", mode="r", encoding="utf8") as infile:
    new_doc = infile.read()

# Tokenize the document
tokens = word_tokenize(new_doc)

# Infer a vector for the document
new_vector = model.infer_vector(tokens)

# Find the most similar documents to the document
similar_docs = model.dv.most_similar([new_vector], topn=5)

# Print the most similar documents
for doc in similar_docs:
    print(doc)
