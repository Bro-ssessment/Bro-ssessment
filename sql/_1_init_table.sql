CREATE TABLE users (
    user_id BIGINT PRIMARY KEY, -- unique identifier for each student
    average_sentiment_score NUMERIC(3)
);

CREATE TABLE classes (
    class_id BIGINT PRIMARY KEY,
    average_sentiment_score NUMERIC(3)
);

CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    class_id BIGINT REFERENCES classes(class_id) NOT NULL,
    user_id BIGINT REFERENCES users(user_id) NOT NULL,
    build_on BIGINT REFERENCES posts(post_id),
    title TEXT,
    content TEXT,
    sentiment_score NUMERIC(3)
);
