-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/IN5CRU
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "transformed_movie_metadata" (
    "adult" BOOLEAN,   NOT NULL,
    "belongs_to_collection" TEXT,   NOT NULL,
    "budget" FLOAT,   NOT NULL,
    "homepage" VARCHAR(255),   NOT NULL,
    "id" INT,   NOT NULL,
    "imdb_id" VARCHAR(50),   NOT NULL,
    "original_language" VARCHAR(50),   NOT NULL,
    "original_title" VARCHAR(255),   NOT NULL,
    "overview" TEXT,   NOT NULL,
    "popularity" FLOAT,   NOT NULL,
    "poster_path" VARCHAR(255),   NOT NULL,
    "release_date" DATE,   NOT NULL,
    "revenue" FLOAT,   NOT NULL,
    "runtime" FLOAT,   NOT NULL,
    "status" VARCHAR(50),   NOT NULL,
    "tagline" TEXT,   NOT NULL,
    "title" VARCHAR(255),   NOT NULL,
    "vote_average" FLOAT,   NOT NULL,
    "vote_count" FLOAT   NOT NULL
);

CREATE TABLE "transformed_genres" (
    "movie_id" INT,   NOT NULL,
    "id" INT,   NOT NULL,
    "name" VARCHAR(255)   NOT NULL
);

CREATE TABLE "cast" (
    "movie_id" INT,   NOT NULL,
    "cast_id" INT,   NOT NULL,
    "character" TEXT,   NOT NULL,
    "credit_id" VARCHAR(255),   NOT NULL,
    "gender" INT,   NOT NULL,
    "id" INT,   NOT NULL,
    "name" VARCHAR(255),   NOT NULL,
    "order" INT,   NOT NULL,
    "profile_path" VARCHAR(255)   NOT NULL
);

CREATE TABLE "crew" (
    "movie_id" INT,   NOT NULL,
    "credit_id" VARCHAR(255),   NOT NULL,
    "department" VARCHAR(255),   NOT NULL,
    "gender" INT,   NOT NULL,
    "id" INT,   NOT NULL,
    "job" VARCHAR(255),   NOT NULL,
    "name" VARCHAR(255),   NOT NULL,
    "profile_path" VARCHAR(255)   NOT NULL
);

CREATE TABLE "production_companies" (
    "movie_id" INT,   NOT NULL,
    "id" INT,   NOT NULL,
    "name" VARCHAR(255)   NOT NULL
);

CREATE TABLE "production_countries" (
    "movie_id" INT,   NOT NULL,
    "iso_3166_1" CHAR(2),   NOT NULL,
    "name" VARCHAR(255)   NOT NULL
);

CREATE TABLE "ratings" (
    "user_id" INT,   NOT NULL,
    "movie_id" INT,   NOT NULL,
    "rating" FLOAT,   NOT NULL,
    "timestamp" BIGINT   NOT NULL
);

CREATE TABLE "keywords" (
    "movie_id" INT,   NOT NULL,
    "keywords" TEXT   NOT NULL
);

ALTER TABLE "transformed_genres" ADD CONSTRAINT "fk_transformed_genres_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

ALTER TABLE "cast" ADD CONSTRAINT "fk_cast_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

ALTER TABLE "crew" ADD CONSTRAINT "fk_crew_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

ALTER TABLE "production_companies" ADD CONSTRAINT "fk_production_companies_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

ALTER TABLE "production_countries" ADD CONSTRAINT "fk_production_countries_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

ALTER TABLE "ratings" ADD CONSTRAINT "fk_ratings_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

ALTER TABLE "keywords" ADD CONSTRAINT "fk_keywords_movie_id" FOREIGN KEY("movie_id")
REFERENCES "transformed_movie_metadata" ("id");

