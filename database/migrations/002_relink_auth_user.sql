-- Jednorazowa migracja powiązań użytkowników.
-- Wymaga wcześniejszego wykonania migracji Django auth.

ALTER TABLE ratings
    DROP FOREIGN KEY fk_ratings_user;

ALTER TABLE interactions
    DROP FOREIGN KEY fk_interactions_user;

ALTER TABLE recommendations
    DROP FOREIGN KEY fk_recommendations_user;


ALTER TABLE ratings
    MODIFY COLUMN user_id INT NOT NULL;

ALTER TABLE interactions
    MODIFY COLUMN user_id INT NOT NULL;

ALTER TABLE recommendations
    MODIFY COLUMN user_id INT NOT NULL;


ALTER TABLE ratings
    ADD CONSTRAINT fk_ratings_user
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE;

ALTER TABLE interactions
    ADD CONSTRAINT fk_interactions_user
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE;

ALTER TABLE recommendations
    ADD CONSTRAINT fk_recommendations_user
    FOREIGN KEY (user_id)
    REFERENCES auth_user(id)
    ON DELETE CASCADE;