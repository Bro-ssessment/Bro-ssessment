import psycopg2

from brossessment.models import Post, postgres_db
import argparse
import sys
import time 
import re
from textblob import TextBlob


#330052 ying, sounds like a reasoanble choice..tl
def main(begin_post_id=0, batch_size=100):
    while True:
        current_chunk = get_chunk(begin_post_id, batch_size)
        
        print(
            "Fetching spell check from {} to {}".format(
                current_chunk[0][0], current_chunk[-1][0]
            )
        )
# post ids 327077, 327079 and 330929 have image tags
        result = {}
        for post in current_chunk:
            post_id = post[0]
            content = post[1]
            if not content:
                continue

            # spell checker 
            try:
                if (post_id != 327077) and (post_id != 327079) and (post_id != 330929):
                    spellcheck_content = spell_check_textBlob(content)
                else:
                    spellcheck_content = content
                update_spellcheck(post_id, spellcheck_content)

        #         result[post_id] = {
        #             "post_id": post_id,
        #             "spellcheck_content": spellcheck_content
        #         }
        #         #print(result[post_id])
            except Exception:
                print("{} fail to fetch sentiment score".format(post_id))

        # # with postgres_db.atomic():
        # #     for key, value in result.items():
        # #         query = Post.update(
        # #             spellcheck_content=value["spellcheck_content"]
        # #         ).where(Post.post_id == key)
        # #         query.execute()

        # #time.sleep(5)  # take a break to prevent rate limit
        begin_post_id = post_id


# TextBlob 

def spell_check_textBlob(content):
    content_blob = TextBlob(content)
    correction = content_blob.correct()
    print('correction complete, insert into DB')
    print(correction)
    return str(correction)


def get_chunk(begin_post_id=0, limit=500):
    # connect
    conn = psycopg2.connect(host="localhost",database="brosessment19")


    # activate cursor 
    cur = conn.cursor()
    #select_query = ("SELECT post_id, content from posts where post_id > %s order by post_id LIMIT %s;", begin_post_id, limit)
    cur.execute("SELECT post_id, content from posts where post_id > %s order by post_id LIMIT %s;", (begin_post_id, limit))
    posts = cur.fetchall()
    return posts

def update_spellcheck(postID, content):
    # connect
    conn = psycopg2.connect(host="localhost",database="brosessment19")
    
    # activate cursor 
    cur = conn.cursor()

    # select table and display 
    cur.execute("UPDATE posts SET spellcheck_content = %s where post_id = %s;", (content, postID))
    conn.commit()
    # close connection 
    cur.close()
    conn.close()
    print('entered successfully')
    
# post ids 327077, 327079 and 330929 have image tags
def get_post(begin_post_id=0, limit=500):
    posts = Post.select(Post.post_id, Post.content).where(
        Post.post_id > begin_post_id).order_by(Post.post_id).limit(limit)
    posts = ("SELECT post_id, content f")
    return posts

if __name__ == '__main__':
    # In case error happen, start from where it broke
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--begin_id", help="The ID of last parsed post ID", default=0
    )
    arg_parser.add_argument("--batch_size", help="Batch size", default=100)
    arguments = arg_parser.parse_args()
    main(arguments.begin_id, arguments.batch_size)


    

main()
