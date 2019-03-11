import time
import six
import argparse

from google.cloud import language_v1
from google.cloud.language_v1 import enums

from brossessment.models import Post, postgres_db
from sentimentAnalysis import SentimentAnalysis

from decimal import getcontext, Decimal


sentiment = SentimentAnalysis()


def main(begin_post_id=0, batch_size=100):

    #sets the decimal precision point to 3
    getcontext().prec = 3
    while True:
        current_chunk = get_chunk(begin_post_id, batch_size)

        print('Fetching sentiment score from {} to {}'.format(current_chunk[0].post_id, current_chunk[-1].post_id))

        result = {}
        for post in current_chunk:
            post_id = post.post_id
            content = post.content

            if not content:
                continue

            # google score
            try:
                google_score, magnitude = analyze_sentiment_google(content)
                vader_polarity = analyze_sentiment_vader(content)
                textBlob_polarity = analyze_sentiment_textBlob(content)
                score =  ((google_score)+ (textBlob_polarity) + (vader_polarity))/3
                #score =  (Decimal(textBlob_polarity) + Decimal(vader_polarity))/2
                result[post_id] = {'post_id': post_id, 'score': score, 'google_sentiment_score': google_score, 'google_sentiment_magnitude': magnitude, 'vader_sentiment_score': vader_polarity, 'textblob_sentiment_score': textBlob_polarity}
                print(result[post_id])
            except Exception:
                print('{} fail to fetch sentiment score'.format(post_id))

        with postgres_db.atomic():
            for key, value in result.items():
                query = Post.update(
                    bro_sentiment=value['score'],
                    google_sentiment_score=value['google_sentiment_score'],
                    google_sentiment_magnitude=value['google_sentiment_magnitude'],
                    textblob_sentiment_score=value['textblob_sentiment_score'],
                    vader_sentiment_score=value['vader_sentiment_score'],



                ).where(Post.post_id == key)
                query.execute()

        time.sleep(5)  # take a break to prevent rate limit
        begin_post_id = current_chunk[-1].post_id


def analyze_sentiment_google(content):
    '''Return the sentiment analysis score and magnitude of content
    '''
    client = language_v1.LanguageServiceClient()

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment

    return sentiment.score, sentiment.magnitude

def analyze_sentiment_textBlob(content):
    '''Return the sentiment analysis score
    '''
    polarity = sentiment.textBlobAnalyses(content)
    return polarity

def analyze_sentiment_vader(content):
    '''Return the sentiment analysis score
    '''
    compound = sentiment.get_compound(content)
    return compound

def get_chunk(begin_post_id=0, limit=500):
    posts = Post.select(Post.post_id, Post.content).where(
        Post.post_id > begin_post_id).order_by(Post.post_id).limit(limit)
    return posts


if __name__ == '__main__':
    # In case error happen, start from where it broke
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--begin_id', help='The ID of last parsed post ID', default=0)
    arg_parser.add_argument('--batch_size', help='Batch size', default=100)
    arguments = arg_parser.parse_args()
    main(arguments.begin_id, arguments.batch_size)
