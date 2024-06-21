-- Table for movies_metadata
CREATE TABLE Movies (
    adult BOOLEAN,
    belongs_to_collection TEXT,
    budget FLOAT,
    homepage VARCHAR(255),
    movie_id INT PRIMARY KEY,
    imdb_id VARCHAR(50),
    original_language VARCHAR(50),
    original_title VARCHAR(255),
    overview TEXT,
    popularity FLOAT,
    poster_path VARCHAR(255),
    release_date DATE,
    revenue FLOAT,
    runtime FLOAT,
    status VARCHAR(50),
    tagline TEXT,
    title VARCHAR(255),
    vote_average FLOAT,
    vote_count FLOAT
);

-- Table for Genres
CREATE TABLE Genres (
    movie_id INT,
    id INT,
    name VARCHAR(255),
    PRIMARY KEY (movie_id, id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

-- Table for Cast
CREATE TABLE "Cast" (
    movie_id INT,
    cast_id INT,
    character TEXT,
    credit_id VARCHAR(255),
    gender INT,
    id INT,
    name VARCHAR(255),
    "order" INT,
    profile_path VARCHAR(255),
    PRIMARY KEY (movie_id, cast_id, id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

CREATE TABLE Crew (
    movie_id INT,
    credit_id VARCHAR(255),
    department VARCHAR(255),
    gender INT,
    id INT,
    job VARCHAR(255),
    name VARCHAR(255),
    profile_path VARCHAR(255),
    PRIMARY KEY (movie_id, department, job, id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

-- Table for Production_Companies
CREATE TABLE Production_Companies (
    movie_id INT,
    id INT,
    name VARCHAR(255),
    PRIMARY KEY (movie_id, id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

-- Table for Production_Countries
CREATE TABLE Production_Countries (
    iso_3166_1 VARCHAR(10),
    name VARCHAR(255),
	movie_id INT,
	PRIMARY KEY (iso_3166_1, name, movie_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);


-- Query to Get a List of All Movies

SELECT movie_id, title, release_date
FROM Movies
LIMIT 10;

-- Query to Get Movies Released After 2000

SELECT movie_id, title, release_date
FROM Movies
WHERE release_date > '2000-01-01'
ORDER BY release_date;

-- Query to Get Movies with a Specific Genre

SELECT m.movie_id, m.title, g.name AS genre
FROM Movies m
JOIN genres g ON m.movie_id = g.movie_id
WHERE g.name = 'Comedy'
LIMIT 10;


-- Query to List All Cast Members for a Specific Movie

SELECT m.movie_id, m.title, c.name AS cast_member, c.character
FROM Movies m
JOIN "Cast" c ON m.movie_id = c.movie_id
WHERE m.title = 'Toy Story'
ORDER BY c.cast_id;

-- Query to Find All Movies by a Specific Director

SELECT m.movie_id, m.title, c.name AS director
FROM Movies m
JOIN Crew c ON m.movie_id = c.movie_id
WHERE c.job = 'Director' AND c.name = 'John Lasseter'
ORDER BY m.release_date;

-- Query to Get All Production Companies for a Specific Movie

SELECT m.movie_id, m.title, p.name AS production_company
FROM Movies m
JOIN Production_Companies p ON m.movie_id = p.movie_id
WHERE m.title = 'Toy Story';

-- Query to Get All Production Countries for a Specific Movie

SELECT m.movie_id, m.title, pc.name AS production_country
FROM Movies m
JOIN Production_Countries pc ON m.movie_id = pc.movie_id
WHERE m.title = 'Toy Story';

