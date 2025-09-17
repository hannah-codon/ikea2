-- init.sql
-- Create the pgvector extension if it doesn't exist
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the items table with a vector column
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    article_id VARCHAR(255) NOT NULL,
    embedding vector(384) -- Specify the dimension of the vector
);