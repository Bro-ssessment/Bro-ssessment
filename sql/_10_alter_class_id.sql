-- Drop foreign constraint
ALTER TABLE posts DROP CONSTRAINT posts_class_id_fkey;

-- Update class_id
UPDATE classes SET class_id = 568 WHERE class_id = 1;
UPDATE classes SET class_id = 833 WHERE class_id = 2;
UPDATE classes SET class_id = 841 WHERE class_id = 3;
UPDATE classes SET class_id = 820 WHERE class_id = 4;
UPDATE classes SET class_id = 830 WHERE class_id = 5;
UPDATE classes SET class_id = 826 WHERE class_id = 6;
UPDATE classes SET class_id = 586 WHERE class_id = 7;
UPDATE posts SET class_id = 568 WHERE class_id = 1;
UPDATE posts SET class_id = 833 WHERE class_id = 2;
UPDATE posts SET class_id = 841 WHERE class_id = 3;
UPDATE posts SET class_id = 820 WHERE class_id = 4;
UPDATE posts SET class_id = 830 WHERE class_id = 5;
UPDATE posts SET class_id = 826 WHERE class_id = 6;
UPDATE posts SET class_id = 586 WHERE class_id = 7;

-- Re-add foreign key constraint
ALTER TABLE posts ADD CONSTRAINT posts_class_id_fkey FOREIGN KEY (class_id) REFERENCES classes(class_id);
