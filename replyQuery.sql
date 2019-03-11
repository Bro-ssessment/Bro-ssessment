CREATE VIEW replies AS
SELECT r3.replyer, r3.replied_to, count(*), sum(r3.wordcount), avg(r3.bro_sentiment)
FROM
    (SELECT p1.post_id as replyer_post_id, p1.user_id as replyer, p2.user_id as replied_to, p1.wordcount, p1.bro_sentiment
    FROM posts p1, posts p2
    where p1.builds_on_id IS NOT NULL and p2.post_id=p1.builds_on_id) r3
GROUP BY r3.replyer, r3.replied_to;
