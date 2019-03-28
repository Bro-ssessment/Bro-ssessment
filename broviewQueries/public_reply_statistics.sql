CREATE VIEW public_reply_statistics as
  SELECT r.c_id as c_id,
         count(r.replyer_post_id) as num_of_replies,
         count(DISTINCT r.replyer) as num_of_unique_replyers,
         count(DISTINCT r.replied_to) as num_of_unique_replyees,
         count(r.replyer_post_id)::decimal/count(DISTINCT r.replyer) as avg_replies_per_replyer,
         avg(r.wordcount) as avg_wordcount,
         min(r.wordcount) as min_wordcount,
         max(r.wordcount) as max_wordcount,
         avg(r.bro_sentiment) as avg_bro_sentiment,
         min(r.bro_sentiment) as min_bro_sentiment,
         max(r.bro_sentiment) as max_bro_sentiment
  FROM replies r
  WHERE r.private=FALSE and r.wordcount>0
  GROUP BY r.c_id;
