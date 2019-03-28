CREATE VIEW replies AS
    SELECT p1.class_id as c_id, p1.post_id as replyer_post_id, p1.user_id as replyer, p2.user_id as replied_to, p1.wordcount,
           p1.bro_sentiment, p1.private as private
        FROM posts p1, posts p2
        where p1.builds_on_id IS NOT NULL and p2.post_id=p1.builds_on_id;
