project-3-team-4
This is a group assignment for Project 3 and Team 4 We are Team of 4 members, and below is the name of the Team Members

Ola Usman
HoHsin Chang
Vaibhav Singh
Michael Elkabas
The file exceeds the limit which can be uploaded to github, the files can be downloaded from the below link on kaggle https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset#:~:text=file_download-,Download,-(239%20MB

Data Engineering attributes consists of:

Data Quality and Consistency:
Challenge: One of the primary challenges was ensuring data quality and consistency across multiple CSV files. For example, some columns contained mixed data types or unexpected null values.
Solution: We applied data cleaning techniques, such as coercing non-numeric values to NaN for numeric columns, removing duplicates, and handling missing values.
Handling JSON Fields:
Challenge: The credits.csv file contained JSON strings for the cast and crew columns, and the movies_metadata.csv file had JSON strings for genres, production_companies, and production_countries. Parsing and normalizing these fields was complex.
Solution: We implemented functions to parse JSON strings and expand them into separate rows, ensuring that the nested data was properly structured for relational database storage.
Data Validation:
Challenge: Ensuring that the data met certain validation criteria (e.g., movie_id should not be null, budget should be a positive number) was crucial for maintaining data integrity.
Solution: We used the great_expectations library to define and enforce validation rules. This helped catch and handle data issues before loading the data into the database.
Managing Large Data Sets:
Challenge: Processing large datasets with millions of rows can be memory-intensive and time-consuming.
Solution: We used efficient data processing techniques and leveraged pandas' low_memory parameter to handle large files. Additionally, we ensured that data transformations were optimized for performance.
Dealing with Non-ASCII Characters:
Challenge: Some text fields contained non-ASCII characters, which could cause issues during data processing and storage.
Solution: We implemented a function to clean text fields by removing non-ASCII characters, ensuring that the data was compatible with the database.
Ensuring Referential Integrity:
Challenge: Maintaining referential integrity across different tables was essential, especially when dealing with foreign key relationships.
Solution: We defined primary and foreign key constraints in the SQL schema to enforce referential integrity. We also ensured that all foreign key references were valid by checking the existence of referenced records before insertion.
Transforming and Normalizing Data:
Challenge: Normalizing nested data structures and ensuring that each entity was properly represented in the database required careful planning and execution.
Solution: We created separate tables for entities like genres, cast, crew, production companies, and production countries, and established appropriate foreign key relationships to link them to the main movies table.
Conclusion
These challenges required careful consideration and application of various data engineering techniques to ensure the data was clean, consistent, and ready for analysis. The solutions implemented helped to streamline the data collection process and ensure the integrity and usability of the data in the final database.

Solution Architecture
Overview
The solution architecture outlines the end-to-end data flow from source to target, including extraction, transformation, loading into a PostgreSQL database, and subsequent retrieval for visualization. The key components of this architecture are:
Data Sources: The raw CSV files containing movie-related data.
ETL Pipeline: The process of extracting, transforming, and loading data into the PostgreSQL database.
Database: PostgreSQL database to store the transformed and cleaned data.
Data Retrieval: Retrieving data from the database for analysis and visualization.
Visualization: Using tools like Python (with libraries such as Matplotlib, Seaborn, or Plotly) or other visualization tools to create visual insights.
Source to Target Data Flow
1. Data Sources
Input Files:
movies_metadata.csv
credits.csv
keywords.csv 

2. ETL Pipeline
Extract:
Load the raw CSV files into pandas DataFrames for initial inspection and processing.
Transform:
Data Cleaning: Handle missing values, remove duplicates, and ensure data type consistency.
JSON Parsing: Expand nested JSON fields (e.g., genres, production_companies, cast, crew) into separate rows and columns.
Normalization: Normalize data into separate tables such as Movies, Genres, Cast, Crew, Production_Companies, and Production_Countries.
Validation: Apply data validation rules using great_expectations to ensure data integrity.
Load:
Create the necessary tables in the PostgreSQL database.
Load the transformed and cleaned data into these tables.
3. Database
PostgreSQL Schema:
Movies Table:
sql

4. Data Retrieval
Querying the Database:
Use SQL queries to retrieve data from the PostgreSQL database for analysis. For example, to get the top 10 movies by revenue:
sql

5. Visualization
Tools: Use Python libraries such as Plotly, 
Retrieve data using a SQL query or a Pandas DataFrame.
Create visualizations to gain insights. For example, plotting the top 10 movies by revenue

Conclusion
The end-to-end solution involves extracting data from raw CSV files, transforming and cleaning it using pandas, validating the data, and loading it into a PostgreSQL database. From there, the data can be queried and visualized using various tools to gain insights and make data-driven decisions. This architecture ensures data integrity, consistency, and usability throughout the entire process.
Tools and Libraries Used Storage
PostgreSQL: Used to store the cleaned and transformed data. PostgreSQL is a powerful, open-source relational database system known for its robustness, scalability, and support for advanced SQL features. It was chosen for its ability to handle complex queries and maintain data integrity through primary and foreign keys.
Processing
Python: The primary programming language used for the ETL pipeline.
pandas: Essential for data manipulation and analysis. It provides data structures like DataFrame, which are ideal for handling tabular data.
great_expectations: A data validation library that was not covered in class. It was chosen for its ability to define and enforce validation rules, ensuring data integrity before loading it into the database.
re: The regular expressions library, used for text cleaning to remove non-ASCII characters and unwanted quotes from text fields.
csv: Used to handle CSV file read and write operations, ensuring proper formatting and escaping of characters.
Visualization
Plotly: A graphing library that makes interactive, publication-quality graphs online. It was chosen for its interactive capabilities and ease of use in Jupyter Notebooks.
Libraries/Tools Highlighted (Not Covered in Class)
1. great_expectations
Why it was chosen: Great Expectations is a powerful tool for data validation, allowing for the definition of validation rules and expectations for datasets. This ensures data quality and integrity before it is loaded into the database.

2. re (Regular Expressions)
Why it was chosen: The re library is crucial for complex string manipulation tasks, such as cleaning text fields to remove non-ASCII characters and unwanted quotes.

Summary
The combination of these tools and libraries provided a robust framework for handling the entire ETL process, from data extraction and cleaning to transformation, validation, and storage, culminating in data visualization. The addition of libraries like great_expectations and re significantly enhanced the data validation and cleaning processes, ensuring high data quality and integrity. These tools were chosen for their specific capabilities that addressed the unique challenges encountered during the project.

