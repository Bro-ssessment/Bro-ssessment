CREATE VIEW class_statistics as
SELECT class_id, count(*) as number_of_posts, sum(wordcount) as total_wordcount,
       avg(wordcount) as average_wordcount, avg(bro_sentiment) as average_bro_sentiment_score,
       max(bro_sentiment) as max_bro_sentiment_score, min(bro_sentiment) as min_bro_sentiment_score
FROM posts
GROUP BY class_id;
