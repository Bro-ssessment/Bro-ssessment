CREATE VIEW class_statistics as
SELECT class_id as c_id, count(DISTINCT user_id) as num_of_distinct_users,
       count(*) as number_of_posts,
       count(*) / count(DISTINCT user_id) as posts_per_user,
       sum(wordcount) as total_wordcount,
       avg(wordcount) as average_wordcount,
       avg(bro_sentiment) as average_bro_sentiment_score,
       max(bro_sentiment) as max_bro_sentiment_score,
       min(bro_sentiment) as min_bro_sentiment_score
FROM posts
WHERE wordcount>0
GROUP BY class_id;
