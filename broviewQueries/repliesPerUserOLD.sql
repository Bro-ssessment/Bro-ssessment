CREATE VIEW replies AS
SELECT r3.replyer as replier_id, r3.replied_to as replied_to_id, count(*) as number_of_replies,
       sum(r3.wordcount) as total_wordcount, avg(r3.wordcount) as average_wordcount, avg(r3.bro_sentiment) as average_bro_sentiment_score,
       max(r3.bro_sentiment) as max_bro_sentiment_score, min(r3.bro_sentiment) as min_bro_sentiment_score
FROM
    (SELECT p1.post_id as replyer_post_id, p1.user_id as replyer, p2.user_id as replied_to, p1.wordcount, p1.bro_sentiment
    FROM posts p1, posts p2
    where p1.builds_on_id IS NOT NULL and p2.post_id=p1.builds_on_id) r3
GROUP BY r3.replyer, r3.replied_to;
