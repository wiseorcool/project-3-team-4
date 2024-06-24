import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, inspect, text
from flask import Flask, jsonify, render_template_string
import plotly.express as px
import pandas as pd

# Create an engine
engine = create_engine('postgresql://postgres:1234@localhost/Movie_Metadata_project', echo=True)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Inspect the database
inspector = inspect(engine)
print(inspector.get_table_names())

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/about')
def about():
    image_url = "https://resizing.flixster.com/PeXxAxzwX9Q_ZO7aBgiwNV2KzKY=/206x305/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p21291560_p_v10_aa.jpg"
    html_content = f'''
    <html>
    <head>
        <title>This is a Presentation for Project 3 Team 4</title>
        <style>
            h1 {{
                font-size: 48px; /* Increase the font size */
            }}
            img {{
                width: 400px; /* Increase the width of the image */
                height: auto; /* Maintain aspect ratio */
            }}
        </style>
    </head>
    <body>
        <h1>Project 3 Team 4</h1>
        <img src="{image_url}" alt="Movie Poster">
    </body>
    </html>
    '''
    return render_template_string(html_content)
   

@app.route('/newruntime')
# Top 10 Movies by Runtime
def newruntime():
    # Create a session
    session = Session()

    # Query to get the top 10 movies by revenue and their runtimes
    sql_movies = text("""
    SELECT title, runtime
    FROM transformed_movie_metadata tmm
    WHERE movie_id IN 
    (
        SELECT movie_id
        FROM transformed_movie_metadata 
        ORDER BY revenue DESC
        LIMIT 10
    );
    """)

    # Query to get the average runtime of all movies
    sql_avg_runtime = text("""
    SELECT round(avg(runtime)::numeric, 2) AS avg_runtime
    FROM transformed_movie_metadata;
    """)

    # Execute the queries
    result_movies = session.execute(sql_movies).fetchall()
    result_avg_runtime = session.execute(sql_avg_runtime).fetchone()
    session.close()

    # Extract average runtime
    avg_runtime = result_avg_runtime[0]

    # Convert movie results to a list of dictionaries
    movies = []
    for row in result_movies:
        movies.append({
            'title': row[0],
            'runtime': row[1]
        })

    # Convert to DataFrame for Plotly
    df = pd.DataFrame(movies)

    # Create a Plotly figure
    fig = px.bar(df, x='title', y='runtime', title='Top 10 Movies - Runtime', labels={'runtime': 'Runtime (minutes)'})

    # Add a horizontal line for the average runtime
    fig.add_shape(
        type='line',
        x0=-0.5,  # Extend line to the left beyond the first bar
        x1=len(df) - 0.5,  # Extend line to the right beyond the last bar
        y0=avg_runtime,
        y1=avg_runtime,
        line=dict(color='Red', dash='dash'),
    )

    # Update layout to include average runtime annotation
    fig.update_layout(
        annotations=[
            dict(
                x=len(df) - 0.5,  # Position the annotation at the right end of the line
                y=avg_runtime,
                xref="x",
                yref="y",
                text=f"Avg Runtime: {avg_runtime} mins",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40
            )
        ]
    )

    # Convert Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template_string('''
        <html>
        <head>
            <title>Top 10 Movies by Runtime</title>
        </head>
        <body>
            <h1>Top 10 Movies by Runtime</h1>
            <div>{{ graph_html | safe }}</div>
        </body>
        </html>
    ''', graph_html=graph_html)

@app.route('/revenuegraph')
# Top 10 Movies by Revenue
def revenue_graph():
    # Create a session
    session = Session()

    # Query to get the top 10 movies by revenue and their formatted revenue
    sql_revenue = text("""
    SELECT original_title, revenue
    FROM transformed_movie_metadata 
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    # Execute the query
    result_revenue = session.execute(sql_revenue).fetchall()
    session.close()

    # Convert results to a list of dictionaries
    revenue_data = []
    for row in result_revenue:
        revenue_data.append({
            'title': row[0],
            'revenue': row[1]
        })

    # Convert to DataFrame for Plotly
    df = pd.DataFrame(revenue_data)

    # Create a Plotly figure
    fig = px.bar(df, x='title', y='revenue', title='Top 10 Movies by Revenue', labels={'revenue': 'Revenue ($)', 'title': 'Title'})

    # Convert Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template_string('''
        <html>
        <head>
            <title>Top 10 Movies by Revenue</title>
        </head>
        <body>
            <h1>Top 10 Movies by Revenue</h1>
            <div>{{ graph_html | safe }}</div>
        </body>
        </html>
    ''', graph_html=graph_html)

@app.route('/toppopularrevenue')
# Top 10 Movies by Popularity and Revenue
def top_movies():
    # Create a session
    session = Session()

    # Combined query to get the top 10 movies by popularity that are also in the top 10 by revenue
    sql_revenue = text("""
    SELECT movie_id
    FROM transformed_movie_metadata
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    sql_popularity = text("""
    SELECT movie_id, original_title, revenue, popularity
    FROM transformed_movie_metadata
    ORDER BY popularity DESC
    LIMIT 10;
    """)

    # Execute the queries
    result_revenue = session.execute(sql_revenue).fetchall()
    result_popularity = session.execute(sql_popularity).fetchall()
    session.close()

    # Convert results to DataFrames
    df_revenue = pd.DataFrame(result_revenue, columns=['movie_id'])
    df_popularity = pd.DataFrame(result_popularity, columns=['movie_id', 'original_title', 'revenue', 'popularity'])

    # Find the intersection of top 10 by revenue and top 10 by popularity
    df_popularity['highlight'] = df_popularity['movie_id'].apply(lambda x: 'Top 10 Revenue & Popular' if x in df_revenue['movie_id'].values else 'Popular')

    # Create a Plotly figure
    fig = px.scatter(df_popularity, x='popularity', y='revenue',
                     size='popularity', color='highlight', hover_name='original_title',
                     title='Top 10 Movies by Popularity,Part of Highest Grossing ',
                     labels={'popularity': 'Popularity', 'revenue': 'Revenue ($)'})

    # Convert Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template_string('''
        <html>
        <head>
            <title>Top 10 Movies by Popularity and Revenue</title>
        </head>
        <body>
            <h1>Top 10 Movies by Popularity and Revenue</h1>
            <div>{{ graph_html | safe }}</div>
        </body>
        </html>
    ''', graph_html=graph_html)

@app.route('/topbudgetrevenue')
# Top 10 Movies by Budget and Revenue
def top_movies_budget_revenue():
    # Create a session
    session = Session()

    # Combined query to get the top 10 movies by Budget that are also in the top 10 by revenue
    sql_revenue = text("""
    SELECT movie_id
    FROM transformed_movie_metadata
    ORDER BY revenue DESC
    LIMIT 10;
    """)

    sql_budget = text("""
    SELECT movie_id, original_title, revenue, budget
    FROM transformed_movie_metadata
    ORDER BY budget DESC
    LIMIT 10;
    """)

    # Execute the queries
    result_revenue = session.execute(sql_revenue).fetchall()
    result_budget = session.execute(sql_budget).fetchall()
    session.close()

    # Convert results to DataFrames
    df_revenue = pd.DataFrame(result_revenue, columns=['movie_id'])
    df_budget = pd.DataFrame(result_budget, columns=['movie_id', 'original_title', 'revenue', 'budget'])

    # Find the intersection of top 10 by revenue and top 10 by popularity
    df_budget['highlight'] = df_budget['movie_id'].apply(lambda x: 'Top 10 Revenue & Budget' if x in df_revenue['movie_id'].values else 'budget')

    # Create a Plotly figure
    fig = px.scatter(df_budget, x='budget', y='revenue',
                     size='budget', color='highlight', hover_name='original_title',
                     title='Top 10 Movies by Budget, also in top 10 Revenue',
                     labels={'budget': 'Budget', 'revenue': 'Revenue ($)'})

    # Convert Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template_string('''
        <html>
        <head>
            <title>Top 10 Movies by Budget and Revenue</title>
        </head>
        <body>
            <h1>Top 10 Movies by Budget and Revenue</h1>
            <div>{{ graph_html | safe }}</div>
        </body>
        </html>
    ''', graph_html=graph_html)

  
# @app.route('/genre_distribution')
# def genre_distribution():
#   # Create a session
#     session = Session()
#     # Query to get the percentage distribution of genres
#     sql_genres = text("""
#     SELECT name, ROUND((count(id) * 100.0 / (SELECT count(*) FROM transformed_genres)), 2) as percentage
#     FROM transformed_genres
#     GROUP BY name
#     ORDER BY percentage DESC;                  
#     """)

# # Query to get genres in the top 10 movies by revenue
#     sql_top_revenue_genres = text("""
#     SELECT DISTINCT tg.name
#     FROM transformed_genres tg
#     WHERE tg.movie_id IN (
#         SELECT tmm.movie_id
#         FROM transformed_movie_metadata tmm
#         ORDER BY tmm.revenue DESC
#         LIMIT 10
#     );
#     """)

#     # Execute the queries
#     result_genres = session.execute(sql_genres).fetchall()
#     result_top_revenue_genres = session.execute(sql_top_revenue_genres).fetchall()
#     session.close()

#     # Extract top revenue genres
#     top_revenue_genres = {row[0] for row in result_top_revenue_genres}

#     # Convert results to a DataFrame for Plotly
#     genres = []
#     for row in result_genres:
#         genres.append({
#             'name': row[0],
#             'percentage': row[1],
#             'highlight': 'Top Revenue' if row[0] in top_revenue_genres else 'Other'
#         })

#     df = pd.DataFrame(genres)

#     # Create a Plotly figure
#     fig = px.icicle(df, path=[px.Constant('Genres'), 'name', 'percentage'], values='percentage',
#                     color='highlight', hover_data=['name'])
#     # fig.show()
#     # Update layout to include legend
#     fig.update_layout(
#         legend_title="Highlight",
#         legend=dict(
#             x=0.75,
#             y=0.99,
#             bgcolor='rgba(255, 255, 255, 0.5)',
#             bordercolor='Black',
#             borderwidth=1
#         )
#     )
#     # Convert Plotly figure to HTML
#     graph_html = fig.to_html(full_html=False)

#     return render_template_string('''
#         <html>
#         <head>
#             <title>Genre Distribution</title>
#         </head>
#         <body>
#             <h1>Percentage Distribution of Movie Genres</h1>
#             <div>{{ graph_html | safe }}</div>
#         </body>
#         </html>
#     ''', graph_html=graph_html)



# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

@app.route('/genre_distribution')
def genre_distribution():
    # Create a session
    session = Session()
    
    # Query to get the percentage distribution of genres
    sql_genres = text("""
    SELECT name, ROUND((count(id) * 100.0 / (SELECT count(*) FROM transformed_genres)), 2) as percentage
    FROM transformed_genres
    GROUP BY name
    ORDER BY percentage DESC;                  
    """)

    # Query to get the genres of the top 10 movies by revenue
    sql_top_revenue_genres = text("""
    SELECT  DISTINCT name
    FROM transformed_genres
    WHERE movie_id IN 
    (
        SELECT movie_id 
        FROM transformed_movie_metadata 
        ORDER by revenue DESC
        LIMIT 10);
    """)

    # Execute the queries
    result_genres = session.execute(sql_genres).fetchall()
    result_top_revenue_genres = session.execute(sql_top_revenue_genres).fetchall()
    session.close()

    # Extract top revenue genres
    top_revenue_genres = {row[0] for row in result_top_revenue_genres}

    # Convert results to a DataFrame for Plotly
    genres = []
    for row in result_genres:
        genres.append({
            'name': row[0],
            'percentage': row[1],
            'highlight': 'Top Revenue' if row[0] in top_revenue_genres else 'Other'
        })

    df = pd.DataFrame(genres)

    # # Create a Plotly figure
    # fig = px.icicle(df, path=[px.Constant('Genres'), 'name', 'percentage'], values='percentage',
    #                 color='highlight', hover_data=['name'],
    #                 color_discrete_map={'Top Revenue': 'red', 'Other': 'blue'})
    

    # fig = px.icicle(df, path=[px.Constant('Genres'), 'name', 'percentage'], values='percentage',
    #                 color='highlight', hover_data=['name'], color_discrete_map={'Top Revenue': 'red', 'Other': 'blue'},
    #                 labels={'highlight': 'Legend'})
    
      
    fig = px.pie(df, values='percentage', names='name', color='highlight',labels='name')
    fig.show()


    # Update the layout to show labels
    fig.update_traces(textinfo='label+percent', hoverinfo='label+percent+name')

    fig.update_layout(
        title='Percentage Distribution of Movie Genres',
        legend_title_text='Genre'
    )

    # fig.update_layout(legend_title_text='Legend')
    # fig.show()


        

    # Convert Plotly figure to HTML
    graph_html = fig.to_html(full_html=False)

    return render_template_string('''
        <html>
        <head>
            <title>Genre Distribution</title>
        </head>
        <body>
            <h1>Percentage Distribution of Movie Genres</h1>
            <div>{{ graph_html | safe }}</div>
        </body>
        </html>
    ''', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


