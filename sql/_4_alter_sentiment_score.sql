ALTER TABLE posts ADD COLUMN google_sentiment_magnitude REAL;
ALTER TABLE posts RENAME COLUMN sentiment_score TO google_sentiment_score;
ALTER TABLE posts ALTER COLUMN google_sentiment_score TYPE REAL;
ALTER TABLE posts ADD COLUMN textblob_sentiment_score REAL;
ALTER TABLE users ALTER COLUMN average_sentiment_score TYPE REAL;
ALTER TABLE classes ALTER COLUMN average_sentiment_score TYPE REAL;
