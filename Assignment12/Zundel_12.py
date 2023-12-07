from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import pos_tag, word_tokenize
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import json


def count_adverbs(tagged_sentence):
    count = 0
    for word, tag in tagged_sentence:
        if tag == 'RB':
            count += 1

    return count


if __name__ == '__main__':
    with open('updated_yelp_AZ_2021.json', 'r') as file:
        data = json.load(file)
    reviews = data['data']

    # with open('reviews.csv', 'w') as outfile:
    #     # Header row
    #     header = ['stars', 'adverbs', 'sentiment']
    #     outfile.write(f"{','.join(header)}\n")
    #
    #     sent_analyzer = SentimentIntensityAnalyzer()
    #     for review in reviews:
    #         stars = str(review['stars'])
    #         text = review['text'].strip()
    #         tagged_sentence = pos_tag(word_tokenize(text))
    #         adverb_count = str(count_adverbs(tagged_sentence))
    #         sentiment = str(sent_analyzer.polarity_scores(text)['compound'])
    #
    #         line = [stars, adverb_count, sentiment]
    #         outfile.write(f"{','.join(line)}\n")

    df = pd.read_csv('reviews.csv')

    stars = df['stars']
    adverbs = df['adverbs']
    sentiment = df['sentiment']

    star_adverb_corr, _ = pearsonr(stars,adverbs)
    star_sentiment_corr, _ = pearsonr(stars, sentiment)

    plt.plot(star_adverb_corr)
    plt.scatter(stars, adverbs)
    plt.title('Correlation between stars and adverbs')
    plt.xlabel('Stars')
    plt.ylabel('Adverbs')
    plt.show()

    plt.plot(star_sentiment_corr)
    plt.scatter(stars, sentiment)
    plt.title('Correlation between stars and sentiment')
    plt.xlabel('Stars')
    plt.ylabel('Sentiment')
    plt.show()






