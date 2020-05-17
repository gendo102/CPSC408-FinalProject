from flask import Flask, render_template, request, redirect, url_for, Response, flash
from wtforms import Form, StringField, SelectField
import os
import pymysql
import io
import csv
import datetime

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

########################## Inserting ############################################
class MovieAddRatingForm(Form):
    table_choices = [('Choose selection:', 'Choose selection:'),
                      ('User Rating', 'User Rating'),
                      ('Actor', 'Actor'),
                      ('Director', 'Director'),
                     ('Movie', 'Movie'), ]
    add_table = SelectField('', choices=table_choices, default=None)

    ###RECOMMENDATIONS
    add_rec_title = StringField("Title", '', default=None)
    user_rating_choices = [('Choose selection:', 'Choose selection:'),
                      ('1', '1'),
                      ('2', '2'),
                      ('3', '3'),
                      ('4', '4'),
                      ('5', '5'),]
    add_user_rating = SelectField("User Rating", choices=user_rating_choices, default=None)

    ###ACTORS
    add_actor_name = StringField("Name", '',  default=None)
    add_actor_age = StringField("Age", '', default=None)
    user_gender_choices = [('Choose selection:', 'Choose selection:'),
                           ('M', 'M'),
                           ('F', 'F'),]
    add_gender_actor = SelectField("Gender", choices=user_gender_choices, default=None)

    ###DIRECTORS
    add_director_name = StringField("Name", '', default=None)
    add_director_age = StringField("Age", '', default=None)
    user_gender_choices = [('Choose selection:', 'Choose Choose selection:'),
                           ('M', 'M'),
                           ('F', 'F'), ]
    add_gender_director = SelectField("Gender", choices=user_gender_choices, default=None)


    ###MOVIE
    category_choices = [('Choose selection:', 'Choose selection:'),
                           ('Movie', 'Movie'),
                           ('TV Show', 'TV Show'),
                            ('Episode', 'Episode'),]
    add_category = SelectField("Categories", choices=category_choices, default=None)
    add_movie_title = StringField("Title", '', default=None)
    add_country = StringField("Country", '', default=None)
    add_release_year = StringField("Release Year", '', default=None)
    add_duration = StringField("Duration", '', default=None)
    add_description = StringField("Description", '', default=None)
    choices_genre = [('Choose selection:', 'Choose selection:'),
                     ('Action', 'Action'), ('Adventure', 'Adventure'),('Animation', 'Animation'),
                     ('Comedy', 'Comedy'),('Crime', 'Crime'),('Documentary', 'Documentary'),
                     ('Drama', 'Drama'),('Family', 'Family'),('Horror', 'Horror'),('Independent', 'Independent'),
                     ('International', 'International'),('Romance', 'Romance'),('Sci-Fi', 'Sci-Fi'),('Sport', 'Sport'), ]
    add_genre = SelectField('Genres', choices=choices_genre)
    choices_rating = [('Choose selection:', 'Choose selection:'),
                      ('TV-Y7', 'TV-Y7'),('TV-G', 'TV-G'),('TV-PG', 'TV-PG'),('TV-MA', 'TV-MA'),
                      ('PG-13', 'PG-13'),('TV-14', 'TV-14'),('R', 'R'),('Not Rated', 'Not Rated'),
                      ('Approved', 'Approved'), ]
    add_rating = SelectField('Ratings', choices=choices_rating)
    platform_choices = [('Choose selection:', 'Choose selection:'),
                        ('Netflix', 'Netflix'),('Disney Plus', 'Disney Plus'),('Hulu', 'Hulu'), ]
    add_platform = SelectField("Platforms", choices=platform_choices, default=None)


@app.route('/index2', methods=['GET', 'POST'])
def index2():
    search = MovieAddRatingForm(request.form)
    if request.method == 'POST':
        return insert(search)
    return render_template('inserting_index.html', form=search)


@app.route('/insert', methods = ['POST'])
def insert(search):
    if request.method == "POST":

        if search.data['add_table'] == 'Recommendation':
            title = request.form['add_rec_title']
            user_rating = request.form['add_user_rating']
            #need to add in conditional for if AtDeleted is null once update it is set up
            cursor.execute("""SELECT * FROM Recommendations WHERE MovieID IN(SELECT MovieID
                                                                           FROM Movies
                                                                           WHERE Title = %s);""", (title,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Recommendation already exists!')
                #can add to redirect to update
                return redirect('/index2')
            else:
                cursor.execute("""INSERT INTO Recommendations(UserRating,MovieId)
                                      SELECT %s, MovieId FROM Movies WHERE Title = %s;""", (user_rating, title,))
                conn.commit()
                flash("Recommendation Record Inserted Successfully")
                return redirect('/Recommendations')

        elif search.data['add_table'] == 'Actor':
            actor_name = request.form['add_actor_name']
            actor_age = request.form['add_actor_age']
            actor_gender = search.data['add_gender_actor']
            cursor.execute("""SELECT *  FROM Actors WHERE ActorName = %s;""", (actor_name,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Actor already exists!')
                return redirect('/index2')
            else:
                cursor.execute("""INSERT INTO Actors(ActorName,Age, Gender)
                                      VALUES (%s, %s, %s);""", (actor_name, actor_age, actor_gender,))
                conn.commit()
                flash("Actor Record Inserted Successfully")
                return redirect('/Actors')

        elif search.data['add_table'] == 'Director':
            director_name = request.form['add_director_name']
            director_age = request.form['add_director_age']
            director_gender = search.data['add_gender_director']
            cursor.execute("""SELECT *  FROM Directors WHERE DirectorName = %s;""", (director_name,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Director already exists!')
                return redirect('/index2')
            else:
                cursor.execute("""INSERT INTO Directors(DirectorName, Age, Gender)
                                      VALUES (%s, %s, %s);""", (director_name, director_age, director_gender,))
                conn.commit()
                flash("Director Record Inserted Successfully")
                return redirect('/Directors')

        elif search.data['add_table'] == 'Movie':
            category = search.data['add_category']
            title = request.form['add_movie_title']
            country = request.form['add_country']
            release_year = request.form['add_release_year']
            duration = request.form['add_duration']
            description = request.form['add_description']
            genre = search.data['add_genre']
            rating = search.data['add_rating']
            platform = search.data['add_platform']

            ###### Testing Triple Join #####
            # cursor.execute("""SELECT * FROM Movies
            # INNER JOIN Genres ON Genres.MovieId = Movies.MovieId
            # INNER JOIN Ratings ON Ratings.MovieId = Genres.MovieId
            # INNER JOIN StreamingService ON Platform.MovieId = Ratings.MovieId
            # WHERE Category=%s,Title=%s,Country=%s,ReleaseYear=%s,Duration=%s,Description=%s,
            #         GenreType=%s,Rating=%s,Platform=%s;""",(category,title,country,release_year,duration,description,genre,rating,platform,))
            # result = cursor.fetchall()
            #
            # if cursor.rowcount != 0:
            #     flash('Movie/TV show already exists!')
            #     return redirect('/index2')
            # else:
            cursor.execute("""INSERT INTO Movies(Category, Title, Country, ReleaseYear, Duration, Description)
                                                  VALUES (%s, %s, %s, %s, %s, %s);""",
                           (category, title, country, release_year, duration, description,))
            cursor.execute("""INSERT INTO Genres(GenreType,MovieId)
                                                  SELECT %s, MovieId FROM Movies WHERE Title = %s;""",
                           (genre, title,))
            cursor.execute("""INSERT INTO Ratings(Rating,MovieId)
                                                              SELECT %s, MovieId FROM Movies WHERE Title = %s;""",
                           (rating, title,))
            cursor.execute("""INSERT INTO StreamingService(Platform,MovieId, DateAdded)
                                                              SELECT %s, MovieId, %s FROM Movies WHERE Title = %s;""",
                           (platform, str(datetime.datetime.now()), title))
            conn.commit()
            flash("Movie Records Inserted Successfully")
            return redirect('/Movies')
###################################################################################

########################## Updating ###############################################
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

########################## Deleting ###############################################
# set DeletedAt = current_date
@app.route('/delete/<string:MovieId>', methods = ['GET'])
def deleteMov(MovieId):
    cursor.execute("""UPDATE Movies SET DeletedAt = current_date WHERE MovieId=%s;""", (MovieId,))
    conn.commit()
    return redirect(url_for('Movies'))
##########################################################################

########################## Exporting ###############################################
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

########################## Searching/Filtering ###############################################
class MovieFilterForm(Form):
    choices_filter = [('Choose filter:', 'Choose filter:'),
               ('Rating', 'Rating'),
               ('Genre', 'Genre'),
               ('Category', 'Category'),
               ('Streaming Service', 'Streaming Service'),]
    select_filter = SelectField('Filter movies by:', choices=choices_filter)

    # cursor.execute("""SELECT DISTINCT Rating FROM Ratings""")
    choices_rating = [('Choose Rating:', 'Choose Rating:'),
                ('TV-Y7', 'TV-Y7'),('TV-G', 'TV-G'),('TV-PG', 'TV-PG'),('TV-MA', 'TV-MA'),('PG-13', 'PG-13'),
                      ('TV-14', 'TV-14'),('R', 'R'),('Not Rated', 'Not Rated'),('Approved', 'Approved'),]
    select_rating = SelectField('Ratings:', choices=choices_rating)

    choices_genre = [('Choose Genre:', 'Choose Genre:'),
                ('Action', 'Action'),('Adventure', 'Adventure'),('Animation', 'Animation'),('Comedy', 'Comedy'),
                ('Crime', 'Crime'),('Documentary', 'Documentary'),('Drama', 'Drama'),('Family', 'Family'),
                ('Horror', 'Horror'),('Independent', 'Independent'),('International', 'International'),
                ('Romance', 'Romance'),('Sci-Fi', 'Sci-Fi'),('Sport', 'Sport'),]
    select_genre = SelectField('Genres:', choices=choices_genre)

    choices_category = [('Choose Category:', 'Choose Category:'),
                ('Movie', 'Movie'),('TV Show', 'TV Show'),('Episode', 'Episode'),]
    select_category = SelectField('Category:', choices=choices_category)

    choices_platform = [('Choose Platform:', 'Choose Platform:'),
                        ('Netflix', 'Netflix'),('Disney Plus', 'Disney Plus'),('Hulu', 'Hulu'), ]
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