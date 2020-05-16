from flask import Flask, render_template, request, redirect, url_for, Response, flash
from wtforms import Form, StringField, SelectField
import os
import pymysql
import io
import csv

app = Flask(__name__, template_folder="Templates")

app.secret_key = '701701'
conn = pymysql.connect("34.83.8.98","root","Hk1ru0HoKkjjzKzv","FinalProject")
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
    return render_template('login.html')

@app.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return 'here'
    return render_template('home.html')

class Content:
    def movies_list(self):
        cursor.execute(
            "SELECT * FROM Movies")
        result = cursor.fetchall()
        return result

    def actors_list(self):
        cursor.execute(
            "SELECT * FROM Actors")
        result = cursor.fetchall()
        return result

    def directors_list(self):
        cursor.execute(
            "SELECT * FROM Directors")
        result = cursor.fetchall()
        return result

    def genres_list(self):
        cursor.execute(
            "SELECT * FROM Genres")
        result = cursor.fetchall()
        return result

    def ratings_list(self):
        cursor.execute(
            "SELECT * FROM Ratings")
        result = cursor.fetchall()
        return result

    def recommendations_list(self):
        cursor.execute(
            "SELECT * FROM Recommendations")
        result = cursor.fetchall()
        return result

    def streamingservice_list(self):
        cursor.execute(
            "SELECT * FROM StreamingService")
        result = cursor.fetchall()
        return result

@app.route('/Movies', methods=['GET','POST'])
def Movies():
    def db_query():
        db = Content()
        movies = db.movies_list()
        return movies
    result = db_query()
    table = 'Movies'
    html_file = 'movies.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/Actors', methods=['GET','POST'])
def Actors():
    def db_query():
        db = Content()
        actors = db.actors_list()
        return actors
    result = db_query()
    table = 'Actors'
    html_file = 'actors.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/Directors', methods=['GET','POST'])
def Directors():
    def db_query():
        db = Content()
        directors = db.directors_list()
        return directors
    result = db_query()
    table = 'Directors'
    html_file = 'directors.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/Genres', methods=['GET','POST'])
def Genres():
    def db_query():
        db = Content()
        genres = db.genres_list()
        return genres
    result = db_query()
    table = 'Genres'
    html_file = 'genres.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/Ratings', methods=['GET','POST'])
def Ratings():
    def db_query():
        db = Content()
        ratings = db.ratings_list()
        return ratings
    result = db_query()
    table = 'Ratings'
    html_file = 'ratings.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/Recommendations', methods=['GET','POST'])
def Recommendations():
    def db_query():
        db = Content()
        recommendations = db.recommendations_list()
        return recommendations
    result = db_query()
    table = 'Recommendations'
    html_file = 'recommendations.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/StreamingService', methods=['GET','POST'])
def StreamingService():
    def db_query():
        db = Content()
        streamingservice = db.streamingservice_list()
        return streamingservice
    result = db_query()
    table = 'StreamingService'
    html_file = 'streamingservice.html'
    return render_template(html_file, result=result, content_type='application/json',data=table)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        Category = request.form['Category']
        Title = request.form['Title']
        Country = request.form['Country']
        ReleaseYear = request.form['ReleaseYear']
        Duration = request.form['Duration']
        Description = request.form['Description']
        cursor.execute("INSERT INTO Movies (Category, Title, Country, ReleaseYear, Duration, Description) VALUES (%s, %s, %s, %s, %s, %s)", (Category, Title, Country, ReleaseYear, Duration, Description))
        conn.commit()
        return redirect(url_for('Movies'))

        MovieId = cursor.lastrowid

        # Actors
        ActorName = request.form['ActorName']
        Gender = request.form['Gender']
        Age = request.form['Age']
        cursor.execute("INSERT INTO Actors(ActorName,Gender,Age)"
                         "VALUES(%s,%s,%s);", (ActorName,Gender,Age))
        conn.commit()
        return redirect(url_for('Actors'))

        """
        # Directors
        cursor.execute("INSERT INTO Directors(DirectorName,Gender,Age)"
                         "VALUES(%s,%s,%s);", (DirectorName,Gender,Age))
        conn.commit()
        
        # make sure other tables are updated with movie ID after inserting into movies
        # Genres
        cursor.execute("INSERT INTO Genres(MovieId, GenreType)"
                         "VALUES(%s,%s);", (MovieId, GenreType))
        conn.commit()
        # Ratings
        cursor.execute("INSERT INTO Ratings(MovieId, Rating)"
                         "VALUES(%s,%s);", (MovieId, Rating))
        conn.commit()
        # Recommendations table is empty upon starting b/c user will input ratings later
        # StreamingService
        cursor.execute("INSERT INTO StreamingService(MovieId, Platform, DateAdded)"
                         "VALUES(%s,%s,%s);", (MovieId, Platform, DateAdded))
        conn.commit()
       """


@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        MovieId = request.form['MovieId']
        Category = request.form['Category']
        Title = request.form['Title']
        Country = request.form['Country']
        ReleaseYear = request.form['ReleaseYear']
        Duration = request.form['Duration']
        Description = request.form['Description']
        cursor.execute("""
               UPDATE Movies
               SET Category=%s,Title=%s,Country=%s,ReleaseYear=%s,Duration=%s,Description=%s
               WHERE MovieId=%s
            """, (Category, Title, Country, ReleaseYear, Duration, Description, MovieId,))
        conn.commit()
        return redirect(url_for('Movies'))

#########################################################################
@app.route('/delete/<string:MovieId>', methods = ['GET'])
def delete(MovieId):
    cursor.execute("UPDATE Movies SET DeletedAt = current_date WHERE MovieId=%s", (MovieId,))
    return redirect(url_for('Movies'))


# @app.route('/delete', methods = ['POST','GET'])
# def delete():
#     if request.method == 'POST':
#         TableName = request.form['TableName']
#         if TableName == 'Movies':
#             MovieId = request.form['MovieId']
#             cursor.execute("UPDATE Movies SET DeletedAt = current_date WHERE MovieId=%s", (MovieId,))
#             return redirect(url_for('Movies'))
##########################################################################

@app.route('/export',methods=['POST','GET'])
def export():
    if request.method == 'POST':
        TableName = request.form['TableName']
        if TableName == 'Movies':
            cursor.execute("SELECT * FROM Movies")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Movie Id','Category','Title','Country','Release Year','Duration','Description','DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=Movies.csv"})
            # return redirect(url_for('Movies'))

        elif TableName == 'Actors':
            cursor.execute("SELECT * FROM Actors")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Actor Id', 'Actor Name', 'Age', 'Gender','DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=Actors.csv"})
            # return redirect(url_for('Actors'))

        elif TableName == 'Directors':
            cursor.execute("SELECT * FROM Directors")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Director Id', 'Director Name', 'Age', 'Gender', 'DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=Directors.csv"})
            # return redirect(url_for('Directors'))

        elif TableName == 'Genres':
            cursor.execute("SELECT * FROM Genres")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Movie Id', 'Genre Type','DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=Genres.csv"})
            # return redirect(url_for('Genres'))

        elif TableName == 'Ratings':
            cursor.execute("SELECT * FROM Ratings")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Movie Id', 'Rating', 'DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=Ratings.csv"})
            # return redirect(url_for('Ratings'))

        elif TableName == 'Recommendations':
            cursor.execute("SELECT * FROM Recommendations")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Movie Id', 'User Rating','DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=Recommendations.csv"})
            # return redirect(url_for('Recommendations'))

        elif TableName == 'StreamingService':
            cursor.execute("SELECT * FROM StreamingService")
            result = cursor.fetchall()
            output = io.StringIO()
            writer = csv.writer(output)
            line = ['Movie Id', 'Platform', 'Date Added', 'DeletedAt']
            writer.writerow(line)
            for row in result:
                writer.writerow(row)
            output.seek(0)
            return Response(output, mimetype="text/csv",
                            headers={"Content-Disposition": "attachment;filename=StreamingService.csv"})
            # return redirect(url_for('StreamingService'))
        else:
            return redirect(url_for('Movies'))

# searching and filtering
class MovieFilterForm(Form):
    choices_filter = [('Choose filter:', 'Choose filter:'),
               ('Rating', 'Rating'),
               ('Genre', 'Genre'),
               ('Category', 'Category'),
               ('Streaming Service', 'Streaming Service'),]
    select_filter = SelectField('Filter movies by:', choices=choices_filter)

    # cursor.execute("""SELECT DISTINCT Rating FROM Ratings""")
    choices_rating = [('Choose Rating:', 'Choose Rating:'),
                ('TV-Y7', 'TV-Y7'),
                ('TV-G', 'TV-G'),
                ('TV-PG', 'TV-PG'),
                ('TV-MA', 'TV-MA'),
                ('PG-13', 'PG-13'),
                ('TV-14', 'TV-14'),
                ('R', 'R'),
                ('Not Rated', 'Not Rated'),
                ('Approved', 'Approved'),]
    select_rating = SelectField('Ratings:', choices=choices_rating)

    choices_genre = [('Choose Genre:', 'Choose Genre:'),
                ('Action', 'Action'),
                ('Adventure', 'Adventure'),
                ('Animation', 'Animation'),
                ('Comedy', 'Comedy'),
                ('Crime', 'Crime'),
                ('Documentary', 'Documentary'),
                ('Drama', 'Drama'),
                ('Family', 'Family'),
                ('Horror', 'Horror'),
                ('Independent', 'Independent'),
                ('International', 'International'),
                ('Romance', 'Romance'),
                ('Sci-Fi', 'Sci-Fi'),
                ('Sport', 'Sport'),]
    select_genre = SelectField('Genres:', choices=choices_genre)


    choices_category = [('Choose Category:', 'Choose Category:'),
                ('Movie', 'Movie'),
                ('TV Show', 'TV Show'),
                ('Episode', 'Episode'),]
    select_category = SelectField('Category:', choices=choices_category)

    choices_platform = [('Choose Platform:', 'Choose Platform:'),
                        ('Netflix', 'Netflix'),
                        ('DisneyPlus', 'DisneyPlus'), ]
    select_platform = SelectField('Platform:', choices=choices_platform)

    choices_search = [('Title', 'Title'),
               ('Year', 'Year'),
               ('Actor', 'Actor'),
               ('Director', 'Director'),
               ('Country', 'Country'),]
    search_options = SelectField('Search for:', choices=choices_search)
    search_field = StringField('')

@app.route('/index', methods=['GET', 'POST'])
def index():
    search = MovieFilterForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('filter_index.html', form=search)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results(search):
   # search_string = search.data['search']
   # if search_string:
    if search.data['select_filter'] == 'Rating':
        search_string = search.data['select_rating']
        cursor.execute("""SELECT *  FROM Movies WHERE MovieID IN(SELECT MovieID 
                                                                    FROM Ratings
                                                                    WHERE Rating = %s) AND DeletedAt IS NULL 
                                                                    ORDER BY Title;""", (search_string,))

        result = cursor.fetchall()

        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type = 'application/json')


    elif search.data['select_filter'] == 'Genre':
        search_string = "%" + request.form['select_genre'] + "%"
       # likeString = "'%" + search_string + "%'"
        cursor.execute("""SELECT *  FROM Movies WHERE MovieID IN(SELECT MovieID 
                                                                       FROM Genres
                                                                       WHERE GenreType LIKE %s) AND DeletedAt IS NULL 
                                                                       ORDER BY Title;""", (search_string,))

        result = cursor.fetchall()

        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['select_filter'] == 'Category':
        search_string = "%" + request.form['select_category'] + "%"
        cursor.execute("""SELECT *  FROM Movies WHERE Category LIKE %s AND DeletedAt IS NULL 
                                                                          ORDER BY Title;""", (search_string,))

        result = cursor.fetchall()

        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['select_filter'] == 'Streaming Service':
        search_string = search.data['select_platform']
        cursor.execute("""SELECT *  FROM Movies WHERE MovieID IN(SELECT MovieID 
                                                                       FROM StreamingService
                                                                       WHERE Platform = %s) AND DeletedAt IS NULL 
                                                                       ORDER BY Title;""", (search_string,))

        result = cursor.fetchall()

        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Title':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Movies WHERE Title LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Year':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Movies WHERE ReleaseYear LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Actor':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Actors WHERE ActorName LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('person_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Director':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Directors WHERE DirectorName LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('person_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Country':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Movies WHERE Country LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/index')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    else:
        flash('No results found!')
        return redirect('/index')

# Main method
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)), debug=True)