from gensim.models.doc2vec import Doc2Vec
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from string import punctuation
from gensim import corpora
import gensim,re,os

def file2str(pathway):
    with open(pathway, encoding="utf8") as infile:
        return infile.read().replace("\n", " ")

def clean(doc):
    doc = ''.join(ch for ch in doc if ch not in exclude or ch != '—')
    doc = " ".join(i for i in doc.lower().split() if i not in stop)
    doc = re.sub(r"([a-z]+)\d+", r"\1", doc)
    doc = " ".join(lemma.lemmatize(word) for word in doc.split())
    return doc

if __name__ == '__main__':
    # Get a list of all the files in the news_universe directory
    os.chdir("news_universe")

    # Only get the .txt files
    filenames = [i for i in os.listdir() if re.search(r"\.txt", i)]

    # Read all the documents
    # This is a list of the string contents of the files
    doc_complete = [file2str(i) for i in filenames]

    # Get rid of all the stopwords and excess punctuation
    stop = stopwords.words('english')
    exclude = punctuation
    exclude = "".join([ch for ch in exclude if not re.search(r"[-']", ch)])
    exclude += "”"
    exclude += "“"
    lemma = WordNetLemmatizer()

    # create a list of cleaned words from each document
    doc_clean = [clean(doc).split() for doc in doc_complete]

    # Creating the term dictionary of our corpus, where every unique term is assigned an index.
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    # Creating the object for LDA model using gensim library
    num_topics = 5
    num_words = 10
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50)
    results = ldamodel.print_topics(num_topics=num_topics, num_words=num_words)

    headers = ['topic', '1st', '2nd','3rd','4th','5th','6th', '7th', '8th', '9th', '10th']
    topics = ['inclusion', 'housing market', 'school news', 'political news', 'local elections']
    with open('../doc_term_frequent.csv', 'w') as outfile:
        outfile.write(f'{",".join(headers)}\n')

        # (0, '0,0111*"pope"')
        for i in range(len(results)):
            # This only takes the values between
            word = re.sub(r'[\w\d\*\.]+\"([^\"]+)\"', r'\1', results[i][1])
            word = word.split(' + ')
            outfile.write(f'{topics[i]},{",".join(word)}\n')
