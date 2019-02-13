from brossessment.models import Post, postgres_db
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import argparse

# source: https://pythonprogramming.net/sentiment-analysis-python-textblob-vader/

analyzer = SentimentIntensityAnalyzer()
threshold = 0.5

class SentimentAnalysis:
    def __init__(self):
        return

    #https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f
    # takes a text input, returns polarity as (negative, neutral, positive)
    def vaderAnalysis(self, text):
        #print(text)
        score = analyzer.polarity_scores(text)
        #print('this is the score')
        #print(str(score))
        #print("{:-<40} {}".format(text, str(score)))
        return str(score)


#https://textblob.readthedocs.io/en/dev/quickstart.html
# goes through list and evaluates each and returns average of everything
    def textBlobAnalysesmulti(self, posts):
        polarity = 0
        lines = 0
        for line in posts:
            post_sentiment = self.textBlobAnalyses(line)
            polarity += post_sentiment
            lines += 1

        average_polarity = polarity/lines
        #print("the polarity of {} is {}".format(posts, average_polarity))

        # returns an average of the polarity of the list
        return average_polarity
# evaluates one post and returns polarity
    def textBlobAnalyses(self, text):
        polarity = 0
        blob = TextBlob(text)
        clean_blob = blob.correct()
        post_sentiment = blob.sentiment.polarity
        polarity += post_sentiment
        #print("the polarity of {} is {}".format(text, polarity))
        return polarity

    def comparisonAnalyses(self, text):
        vader = self.vaderAnalysis(text)
        textBlob = self.textBlobAnalyses(text)
        vader_score = self.get_compound(vader)
        return (textBlob - vader_score)

    def get_compound(self, text):
        vader_text = self.vaderAnalysis(text)
        compound = vader_text.find('compound')
        return (float(vader_text[compound + 11:-1]))
