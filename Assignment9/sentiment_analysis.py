from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords as sw
import json
import re

def sort_counts(dictionary):
  # Getting a list of tuples like (word, count)
  word_count = list(dictionary.items())
  # Sorting word_count by the count from highest to lowest
  word_count.sort(key=lambda i:i[1], reverse=True)
  return word_count


if __name__ == "__main__":
    # Initialize class for sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    video_id = "ZZ5LpwO-An4"  # Heyayayayay video

    # Load the YouTube comments into elements
    with open(f'youtube_comments_{video_id}.json', 'r', encoding='utf-8') as file:
        elements = json.load(file)

    sentence_count = []
    sentiment_word_count ={}
    # Loop through all the comments
    for comment in elements['comments']:
        # Get the overall sentiment of the sentence
        sent = analyzer.polarity_scores(comment)

        # If the sentiment is greater than 0.05, then it is generally positive
        if sent['compound'] >= 0.05:
            sentence_count.append(comment)
            # Replacing most extra characters with a space
            comment = re.sub('[@\\\:\*\',.\"\(\)\?\!]', ' ', comment)
            # Replacing a dash with nothing to retain hyphenated words
            comment = re.sub('\-', '', comment)

            # Changing the sentence to lowercase, getting rid of white space, and return a list of words
            words = comment.lower().strip().split()

            # Looping through all the cleaned words
            for word in words:
                # Filter out the stopwords
                if word in sw.words():
                    continue
                # Initialize word in sentiment word count dictionary if it isn't in there already
                if word not in sentiment_word_count:
                    sentiment_word_count[word] = 0
                sentiment_word_count[word] += 1

    # Returns a list of all the sorted words from the word count dictionary
    sorted_word_counts = sort_counts(sentiment_word_count)

    # Prints out the first 5 elements of the list
    print(sorted_word_counts[:5])
    print(len(sentence_count))

