import time
import six
import argparse
import nltk
from collections import Counter


from brossessment.models import Post, postgres_db


def main(begin_post_id=0, batch_size=100):
    while True:
        current_chunk = get_chunk(begin_post_id, batch_size)

        print('Fetching Fetching verb and noun count from {} to {}'.format(current_chunk[0].post_id, current_chunk[-1].post_id))

        result = {}
        for post in current_chunk:
            post_id = post.post_id
            content = post.content
            #print(content)

            if not content:
                continue

            try:
                pos_dict = analyze_pos(content)
                #print(pos_dict['JJ'])
                
                
            except Exception:
             
                print('{} fail to fetch verb and noun count'.format(post_id))

            result[post_id] = {'verbs': pos_dict['verbs'], 'nouns': pos_dict['nouns'], 'adjectives': pos_dict['adjectives']}
            print(result[post_id])

        with postgres_db.atomic():
            print('these are teh results')
            print(result)
            print(result.items())
            print(result.keys())
            for key, value in result.items():
                print('this is the key')
                print(key)
                print('this is the value')
                print(value)
                print(value['verbs'])
                try:
                    query = Post.update(
                        verbs=value['verbs'],
                        nouns=value['nouns'],
                        adjectives=value['adjectives']
                    ).where(Post.post_id == key)
                    #query.execute()
                    print("successfully added to ")
                    print(post_id)
                except Exception as e:
                    print(e)
                    print('failed to add pos tag to ')
                    print(post_id)
                    continue

        time.sleep(5)  # take a break to prevent rate limit
        begin_post_id = current_chunk[-1].post_id


def analyze_pos(content):
    '''Return the sentiment analysis score and magnitude of content
    '''
 
    tokens = nltk.word_tokenize(content)
    text = nltk.Text(tokens)
    tagged = nltk.pos_tag(text)
    pos_dict = {'verbs':0, 'nouns':0, 'adjectives':0, 'others':0}
    for pos in tagged:
        
        if (pos[1][0].upper()) == 'V':
            pos_dict['verbs'] += 1
        elif (pos[1][0].upper()) == 'N':
            pos_dict['nouns'] += 1
        
        elif (pos[1][0].upper()) == 'J':
            pos_dict['adjectives'] += 1
        
        else:
            pos_dict['others'] += 1 

    total = sum(pos_dict.values())
    tokens_dict = dict((word, float(count)/total) for word,count in pos_dict.items()) 
    return(tokens_dict)



    


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
