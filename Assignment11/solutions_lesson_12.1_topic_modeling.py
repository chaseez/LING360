"""Script to do some topic modeling
Earl K. Brown, ekbrown@byu.edu
cf. https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/
"""

### GET ALL FILES IN LIST ###
def file2str(pathway):
    with open(pathway, encoding="utf8") as infile:
        return infile.read().replace("\n", " ")

import os, re
os.chdir("../Assignment10")
filenames = [i for i in os.listdir() if re.search(r"\.txt", i)]

doc_complete = [file2str(i) for i in filenames]

### CLEAN UP LIST OF FILES ###
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop = stopwords.words('english')
exclude = string.punctuation
exclude = "".join([ch for ch in exclude if not re.search(r"[-']", ch)])
exclude += "”"
exclude += "“"
lemma = WordNetLemmatizer()
def clean(doc):
    doc = ''.join(ch for ch in doc if ch not in exclude)
    doc = " ".join(i for i in doc.lower().split() if i not in stop)
    doc = re.sub(r"([a-z]+)\d+", r"\1", doc)
    doc = " ".join(lemma.lemmatize(word) for word in doc.split())
    return doc

doc_clean = [clean(doc).split() for doc in doc_complete]
doc_clean = [[wd for wd in doc if wd != "u"] for doc in doc_clean]

### GET TOPICS ###
import gensim
from gensim import corpora

# Creating the term dictionary of our corpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
num_topics = 5
num_words = 5
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50)
results = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)
for r in results:
    print(r)

### VISUALIZE THE TOPICS ###

# interactive display with D3 javascript library
import pyLDAvis
import pyLDAvis.gensim_models
visualization = pyLDAvis.gensim_models.prepare(ldamodel, doc_term_matrix, dictionary)
pyLDAvis.save_html(visualization, "../Assignment11/visualization.html")

# version 2.1.2 of pyLDAvis
# import pyLDAvis
# import pyLDAvis.gensim
# to_show = pyLDAvis.gensim.prepare(ldamodel, doc_term_matrix, dictionary)
# pyLDAvis.show(to_show)

"""
THIS SECTION IS COMMENTED OUT WITH THE TRIPLE DOUBLE QUOTES ABOVE AND AT THE END OF THE SCRIPT

### ForceAtlas2 algorithm (code from Rob Reynolds: https://github.com/reynoldsnlp/F18_DIGHT360/blob/master/activities/12_04_topic_modeling.py)

from fa2 import ForceAtlas2  # pip install fa2
import matplotlib.pyplot as plt
import networkx as nx

rows = []
for i in range(0, len(doc_term_matrix)):
    doc_topics = ldamodel.get_document_topics(doc_term_matrix[i])
    for topic in doc_topics:
        row = [filenames[i], topic[0], topic[1]]
        rows.append(row)

edges = [(i[0][8:-5], i[1], i[2]) for i in rows]

g = nx.Graph()
g.add_weighted_edges_from(edges)
# print(g.edges())

forceatlas2 = ForceAtlas2(# Behavior alternatives  # noqa: E261
                          outboundAttractionDistribution=False,  # Dissuade hubs
                          linLogMode=False,  # NOT IMPLEMENTED
                          adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                          edgeWeightInfluence=1.0,

                          # Performance
                          jitterTolerance=1.0,  # Tolerance
                          barnesHutOptimize=True,
                          barnesHutTheta=1.2,
                          multiThreaded=False,  # NOT IMPLEMENTED

                          # Tuning
                          scalingRatio=2.0,
                          strongGravityMode=False,
                          gravity=4.0,

                          # Log
                          verbose=True)

positions = forceatlas2.forceatlas2_networkx_layout(g, pos=None, iterations=2000)
print(positions)
nx.draw_networkx(g, positions, cmap=plt.get_cmap('jet'), node_size=75, with_labels=True, font_size=8, label=f'Topics')
plt.show()
"""
