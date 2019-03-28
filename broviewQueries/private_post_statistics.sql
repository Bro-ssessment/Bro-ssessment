CREATE VIEW private_post_statistics as
SELECT p.class_id as c_id, avg(p.wordcount) as avg_wc, min(p.wordcount) as min_wc, max(p.wordcount) as max_wc,
       avg(p.bro_sentiment) as avg_bs, min(p.bro_sentiment) as min_bs, max(p.bro_sentiment) as max_bs,
       count(*) as num_of_private_posts
FROM
(SELECT class_id, wordcount, bro_sentiment FROM posts where private=TRUE and wordcount>0) p
GROUP BY c_id;
