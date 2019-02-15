import time
import six
import argparse

from brossessment.models import Post, postgres_db
from sentimentAnalysis import SentimentAnalysis

sentiment = SentimentAnalysis()
def main(begin_post_id=0, batch_size=100):
    while True:
        current_chunk = get_chunk(begin_post_id, batch_size)

        #print('Fetching sentiment score from {} to {}'.format(current_chunk[0].post_id, current_chunk[-1].post_id))

        result = {}
        for post in current_chunk:
            post_id = post.post_id
            content = post.content

            if not content:
                continue

            try:
                polarity = analyze_sentiment(content)
                result[post_id] = {'post_id': post_id, 'polarity': polarity}
                #print(result[post_id])
            except Exception:
                print('{} fail to fetch sentiment score'.format(post_id))



        with postgres_db.atomic():
            for key, value in result.items():
                query = Post.update(
                     textblob_sentiment_score=value['polarity'],

                ).where(Post.post_id == key)
                query.execute()

        time.sleep(5)  # take a break to prevent rate limit
        begin_post_id = current_chunk[-1].post_id


def analyze_sentiment(content):
    '''Return the sentiment analysis score
    '''
    polarity = sentiment.textBlobAnalyses(content)
    return polarity


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
