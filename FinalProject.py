from flask import Flask, render_template, request, redirect, url_for, Response, flash
from wtforms import Form, StringField, SelectField, widgets, SelectMultipleField
from flask_wtf import FlaskForm
import os
import pymysql
import io
import csv
import datetime

app = Flask(__name__, template_folder="Templates")
app.secret_key = '701701'
conn = pymysql.connect("34.83.8.98","root","PASSWORD","FinalProject")
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
            "SELECT MovieId,Category,Title,Country,ReleaseYear,Duration,Description FROM Movies WHERE DeletedAt IS NULL")
        result = cursor.fetchall()
        return result

    def actors_list(self):
        cursor.execute(
            "SELECT ActorId,ActorName,Age,Gender FROM Actors WHERE DeletedAt IS NULL")
        result = cursor.fetchall()
        return result

    def directors_list(self):
        cursor.execute(
            "SELECT DirectorId,DirectorName,Age,Gender FROM Directors WHERE DeletedAt IS NULL")
        result = cursor.fetchall()
        return result

    def genres_list(self):
        cursor.execute(
            "SELECT MovieId,GenreType FROM Genres WHERE DeletedAt IS NULL")
        result = cursor.fetchall()
        return result

    def ratings_list(self):
        cursor.execute(
            "SELECT MovieId,Rating FROM Ratings WHERE DeletedAt IS NULL")
        result = cursor.fetchall()
        return result

    def recommendations_list(self):
        cursor.execute(
            "SELECT MovieId,UserRating FROM Recommendations WHERE DeletedAt IS NULL")
        result = cursor.fetchall()
        return result

    def streamingservice_list(self):
        cursor.execute(
            "SELECT MovieId,Platform,DateAdded FROM StreamingService WHERE DeletedAt IS NULL")
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
                     ('Movie/TV Show/Episode', 'Movie/TV Show/Episode'), ]
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
    user_gender_choices = [('Choose selection:', 'Choose selection:'),
                           ('M', 'M'),
                           ('F', 'F'), ]
    add_gender_director = SelectField("Gender", choices=user_gender_choices, default=None)


    ###MOVIE/TV SHPOW/EPISODE
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

        if search.data['add_table'] == 'User Rating':
            title = request.form['add_rec_title']
            user_rating = request.form['add_user_rating']
            #need to add in conditional for if AtDeleted is null once update it is set up
            cursor.execute("""SELECT * FROM Recommendations WHERE MovieID IN(SELECT MovieID
                                                                           FROM Movies
                                                                           WHERE Title = %s AND DeletedAt IS NULL);""", (title,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Recommendation already exists!')
                #can add to redirect to update
                return redirect('/index2')
            else:
                cursor.execute("""INSERT INTO Recommendations(UserRating,MovieId)
                                      SELECT %s, MovieId FROM Movies WHERE Title = %s AND DeletedAt IS NULL;""", (user_rating, title,))
                conn.commit()
                flash("Recommendation Record Inserted Successfully")
                return redirect('/index2')


        elif search.data['add_table'] == 'Actor':
            actor_name = request.form['add_actor_name']
            actor_age = request.form['add_actor_age']
            actor_gender = search.data['add_gender_actor']
            cursor.execute("""SELECT *  FROM Actors WHERE ActorName = %s AND DeletedAt IS NULL;""", (actor_name,))
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
            cursor.execute("""SELECT *  FROM Directors WHERE DirectorName = %s AND DeletedAt IS NULL;""", (director_name,))
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

        elif search.data['add_table'] == 'Movie/TV Show/Episode':
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
            cursor.execute("""SELECT * FROM Movies
                                INNER JOIN Genres ON(Movies.MovieId = Genres.MovieId)
                                INNER JOIN Ratings ON(Movies.MovieId = Ratings.MovieId)
                                INNER JOIN StreamingService on (StreamingService.MovieId= Movies.MovieId)
                                WHERE Title = %s AND Movies.DeletedAt IS NULL;""",(title,))
            result = cursor.fetchall()

            if cursor.rowcount != 0:
                flash('Movie/TV/Episode show already exists!')
                return redirect('/index2')
            else:
                cursor.execute("""INSERT INTO Movies(Category, Title, Country, ReleaseYear, Duration, Description)
                                                  VALUES (%s, %s, %s, %s, %s, %s);""",
                           (category, title, country, release_year, duration, description,))
                cursor.execute("""INSERT INTO Genres(GenreType,MovieId)
                                                  SELECT %s, MovieId FROM Movies WHERE Title = %s AND DeletedAt IS NULL;""",
                           (genre, title,))
                cursor.execute("""INSERT INTO Ratings(Rating,MovieId)
                                                              SELECT %s, MovieId FROM Movies WHERE Title = %s AND DeletedAt IS NULL;""",
                           (rating, title,))
                cursor.execute("""INSERT INTO StreamingService(Platform,MovieId, DateAdded)
                                                              SELECT %s, MovieId, %s FROM Movies WHERE Title = %s AND DeletedAt IS NULL;""",
                           (platform, str(datetime.datetime.now()), title))
                conn.commit()
                flash("Movie/TV Show/Episode Records Inserted Successfully")
                return redirect('/Movies')

        else:
            conn.rollback()
            return ('Rollback')
###################################################################################

########################## Updating ###############################################
class SimpleForm2(FlaskForm):
    update_field_category = StringField('Category:','')
    update_field_title = StringField('Title:', '')
    update_field_country = StringField('Country:''')
    update_field_release_year = StringField('Release Year:','')
    update_field_duration = StringField('Duration:', '')
    update_field_description = StringField('Description:','')
    update_field_genre = StringField('Genre:', '')
    update_field_tv_rating = StringField('TV Rating:','')
    update_field_user_rating = StringField('User Rating:', '')
    update_field_platform = StringField('Streaming Service:','')


@app.route('/update', methods = ['GET', 'POST'])
def update():
    form = SimpleForm2()
    if form.validate_on_submit():
        category = request.form['update_field_category']
        title = request.form['update_field_title']
        country = request.form['update_field_country']
        release_year = request.form['update_field_release_year']
        duration = request.form['update_field_duration']
        description = request.form['update_field_description']
        genre = request.form['update_field_genre']
        tv_rating = request.form['update_field_tv_rating']
        user_rating = request.form['update_field_user_rating']
        platform = request.form['update_field_platform']

        cursor.execute("""SELECT Title FROM Movies WHERE Title LIKE %s AND DeletedAt IS NULL;""",(title,))

        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/update')
        else:
            cursor.execute("""UPDATE Movies SET Category = %s, Title = %s, Country = %s, ReleaseYear = %s, Duration = %s, Description = %s WHERE Title = %s;""", (category, title, country, release_year, duration, description, title,))
            cursor.execute("""UPDATE Genres LEFT JOIN Movies ON(Movies.MovieId = Genres.MovieId) SET Genres.GenreType = %s WHERE Movies.Title = %s;""", (genre, title,))
            cursor.execute("""UPDATE Ratings LEFT JOIN Movies ON(Movies.MovieId = Ratings.MovieId) SET Ratings.Rating = %s WHERE Movies.Title = %s;""",(tv_rating, title,))
            cursor.execute("""UPDATE Recommendations LEFT JOIN Movies ON(Movies.MovieId = Recommendations.MovieId) SET Recommendations.UserRating = %s WHERE Movies.Title = %s;""",(user_rating, title,))
            cursor.execute("""UPDATE StreamingService LEFT JOIN Movies ON(Movies.MovieId = StreamingService.MovieId) SET StreamingService.Platform = %s, DateAdded = current_date WHERE Movies.Title = %s;""",(platform, title,))
            conn.commit()

            cursor.execute("""SELECT Movies.*, GenreType, Rating, Platform, DateAdded, UserRating FROM Movies LEFT JOIN Genres ON (Movies.MovieId = Genres.MovieId) LEFT JOIN Ratings ON (Movies.MovieId = Ratings.MovieId) LEFT JOIN StreamingService ON (StreamingService.MovieId= Movies.MovieId) LEFT JOIN Recommendations ON (Recommendations.MovieId= Movies.MovieId) WHERE Title = %s;""",(title,))
            result = cursor.fetchall()
            return render_template('complete_movie_search_results.html', result=result,
                content_type='application/json')

    else:
        return render_template('update.html', form=form)

########################## Deleting ###############################################
# set DeletedAt = current_date
@app.route('/delete/<string:MovieId>', methods = ['GET'])
def deleteMov(MovieId):
    cursor.execute("""UPDATE Movies SET DeletedAt = current_date WHERE MovieId=%s;""", (MovieId,))
    cursor.execute("""UPDATE Genres SET DeletedAt = current_date WHERE MovieId=%s;""", (MovieId,))
    cursor.execute("""UPDATE Ratings SET DeletedAt = current_date WHERE MovieId=%s;""", (MovieId,))
    cursor.execute("""UPDATE Recommendations SET DeletedAt = current_date WHERE MovieId=%s;""", (MovieId,))
    cursor.execute("""UPDATE StreamingService SET DeletedAt = current_date WHERE MovieId=%s;""", (MovieId,))
    conn.commit()
    return redirect(url_for('Movies'))

@app.route('/deleteAct/<string:ActorId>', methods = ['GET'])
def deleteAct(ActorId):
    cursor.execute("""UPDATE Actors SET DeletedAt = current_date WHERE ActorId=%s;""", (ActorId,))
    conn.commit()
    return redirect(url_for('Actors'))

@app.route('/deleteDir/<string:DirectorId>', methods = ['GET'])
def deleteDir(DirectorId):
    cursor.execute("""UPDATE Directors SET DeletedAt = current_date WHERE DirectorId=%s;""", (DirectorId,))
    conn.commit()
    return redirect(url_for('Directors'))
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
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    ###CATEGORIES
    string_of_categories = ['Movie\r\nTV_Show\r\nEpisode\r\n']
    list_of_categories = string_of_categories[0].split()
    # create a list of value/description tuples
    categories_files = [(x, x) for x in list_of_categories]
    categories_enter = MultiCheckboxField(choices=categories_files)

    ###TV RATINGS
    string_of_ratings = ['TV-Y7\r\nTV-G\r\nTV-PG\r\nTV-MA\r\nPG-13\r\nTV-14\r\nR\r\nNot-Rated\r\nApproved\r\n']
    list_of_ratings = string_of_ratings[0].split()
    # create a list of value/description tuples
    ratings_files = [(x, x) for x in list_of_ratings]
    ratings_enter = MultiCheckboxField('Label', choices=ratings_files)

    ###COUNTRIES
    string_of_countries = [
        'Argentina\r\nAustralia\r\nAustria\r\nBrazil\r\nBulgaria\r\nCanada\r\nChile\r\nChina\r\nColombia\r\n'
        'Denmark\r\nEgypt\r\nFinland\r\nFrance\r\nGermany\r\nHong Kong\r\nHungary\r\nIndia\r\nIreland\r\n'
        'Israel\r\nItaly\r\nJapan\r\nMexico\r\nNetherlands\r\nNew_Zealand\r\nNigeria\r\nNorway\r\nPakistan\r\nPeru\r\n'
        'Philippines\r\nRomania\r\nSouth Korea\r\nSpain\r\nSweden\r\nSwitzerland\r\nTanzania\r\nThailand\r\n'
        'Turkey\r\nUnited_Kingdom\r\nUnited_States\r\nVietnam\r\n']
    list_of_countries = string_of_countries[0].split()
    countries_files = [(x, x) for x in list_of_countries]
    countries_enter = MultiCheckboxField('Label', choices=countries_files)

    ###GENRES
    string_of_genres = ['Action\r\nAdventure\r\nAnimation\r\nComedies\r\nCrime\r\nDocumentaries\r\nDramas\r\nFamily\r\nHorror\r\nIndependent\r\nRomantic\r\nSci-Fi\r\nSports\r\n']
    list_of_genres = string_of_genres[0].split()
    # create a list of value/description tuples
    genre_files = [(x, x) for x in list_of_genres]
    genre_enter = MultiCheckboxField('Label', choices=genre_files)

    ###STREAMING SERVICES
    string_of_platforms = ['Netflix\r\nDisney+\r\nHulu\r\n']
    list_of_platforms = string_of_platforms[0].split()
    # create a list of value/description tuples
    platforms_files = [(x, x) for x in list_of_platforms]
    platforms_enter = MultiCheckboxField('Label', choices=platforms_files)

    ###SEARCHING
    choices_search = [('Choose selection: ', 'Choose selection:'),
                      ('Title', 'Title'),
                      ('Year', 'Year'),
                      ('Actor', 'Actor'),
                      ('Director', 'Director'),
                      ('User Rating', 'User Rating')]
    search_options = SelectField('Search for:', choices=choices_search)
    search_field = StringField('')


@app.route('/index', methods=['post', 'get'])
def index():
    form = SimpleForm()
    if form.validate_on_submit():

        ###CATEGORIES
        if not form.categories_enter.data:
            categories = ['Movie', 'TV Show', 'Episode']
        elif form.categories_enter.data == ['TV_Show']:
            categories = ['TV Show']
        else:
            categories = form.categories_enter.data

        ###TV RATINGS
        if not form.ratings_enter.data:
            entered_ratings = ['TV-Y7', 'TV-G', 'TV-PG', 'TV-MA', 'PG-13', 'TV-14', 'R', 'Not Rated', 'Approved']
        else:
            entered_ratings = form.ratings_enter.data


        ###COUNTRIES
        countries_list = []
        if not form.countries_enter.data:
            all_countries_list = ['Argentina', 'Australia', 'Austria', 'Brazil', 'Bulgaria', 'Canada',
                               'Chile', 'China', 'Colombia', 'Denmark', 'Denmark', 'Egypt', 'Finland', 'France',
                               'Germany', 'Hong Kong', 'Hungary', 'India', 'Ireland', 'Israel', 'Italy', 'Japan',
                               'Mexico', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Pakistan', 'Peru',
                               'Philippines', 'Romania', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Tanzania', 'Thailand',
                               'Turkey', 'United Kingdom', 'United States', 'Vietnam']
            for i in range(len(all_countries_list)):
                next_list = '%' + all_countries_list[i] + '%'
                countries_list.append(next_list)
        else:
            countries_list_1 = []
            entered_countries = form.countries_enter.data

            for i in range(len(entered_countries)):
                next_list = '%' + entered_countries[i] + '%'
                countries_list_1.append(next_list)
                if len(countries_list_1) < 42:
                    for i in range(42 - len(entered_countries)):
                        countries_list_1.append(' '' ')
                        countries_list = countries_list_1
                    else:
                        countries_list = countries_list_1
        ###GENRES
        genre_list = []
        if not form.genre_enter.data:
            all_genre_list = ['Action', 'Adventure', 'Animation', 'Comedies', 'Crime', 'Documentaries', 'Dramas', 'Family', 'Horror', 'Independent', 'Romantic', 'Sci-Fi', 'Sports']
            for i in range(len(all_genre_list)):
                next_list = '%' + all_genre_list[i] + '%'
                genre_list.append(next_list)
        else:
            genre_list_1 = []
            entered_genres = form.genre_enter.data

            for i in range(len(entered_genres)):
                next_list = '%' + entered_genres[i] + '%'
                genre_list_1.append(next_list)
            if len(genre_list_1) < 13:
                for i in range(13 - len(entered_genres)):
                    genre_list_1.append(' '' ')
                genre_list = genre_list_1
            else:
                genre_list = genre_list_1

        ###STREAMING SERVICES
        if not form.platforms_enter.data:
            platforms = ['Netflix', 'Disney Plus', 'Hulu']
        elif form.platforms_enter.data == ['Disney+']:
            platforms = ['Disney Plus']
        else:
            platforms = form.platforms_enter.data

        if request.form['search_options'] == 'Title':
            search_string = "%" + request.form['search_field'] + "%"
            cursor.execute("""SELECT Movies.*, GenreType, Rating, Platform, DateAdded, UserRating FROM Movies LEFT JOIN Genres ON (Movies.MovieId = Genres.MovieId) LEFT JOIN Ratings ON (Movies.MovieId = Ratings.MovieId) LEFT JOIN StreamingService ON (StreamingService.MovieId= Movies.MovieId) LEFT JOIN Recommendations ON (Recommendations.MovieId= Movies.MovieId) WHERE Title LIKE %s AND Movies.DeletedAt IS NULL;""",
                (search_string,))
            result = cursor.fetchall()
            if cursor.rowcount == 0:
                flash('No results found!')
                return redirect('/index')
            else:
                return render_template('complete_movie_search_results.html', result=result, content_type='application/json')

        elif request.form['search_options'] == 'Year':
            search_string = "%" + request.form['search_field'] + "%"
            cursor.execute("""SELECT Movies.*, GenreType, Rating, Platform, DateAdded, UserRating FROM Movies LEFT JOIN Genres ON (Movies.MovieId = Genres.MovieId) LEFT JOIN Ratings ON (Movies.MovieId = Ratings.MovieId) LEFT JOIN StreamingService ON (StreamingService.MovieId= Movies.MovieId) LEFT JOIN Recommendations ON (Recommendations.MovieId= Movies.MovieId) WHERE ReleaseYear LIKE %s AND Movies.DeletedAt IS NULL;""",
                (search_string,))
            result = cursor.fetchall()
            if cursor.rowcount == 0:
                flash('No results found!')
                return redirect('/index')
            else:
                return render_template('complete_movie_search_results.html', result=result, content_type='application/json')

        elif request.form['search_options'] == 'Actor':
            search_string = "%" + request.form['search_field'] + "%"
            cursor.execute("""SELECT * FROM Actors WHERE ActorName LIKE %s AND DeletedAt IS NULL;""", (search_string,))
            result = cursor.fetchall()
            if cursor.rowcount == 0:
                flash('No results found!')
                return redirect('/index')
            else:
                return render_template('person_search_results.html', result=result, content_type='application/json')

        elif request.form['search_options'] == 'Director':
            search_string = "%" + request.form['search_field'] + "%"
            cursor.execute("""SELECT * FROM Directors WHERE DirectorName LIKE %s AND DeletedAt IS NULL;""", (search_string,))
            result = cursor.fetchall()
            if cursor.rowcount == 0:
                flash('No results found!')
                return redirect('/index')
            else:
                return render_template('person_search_results.html', result=result, content_type='application/json')

        elif request.form['search_options'] == 'User Rating':
            search_string = request.form['search_field']
            cursor.execute(
                """SELECT Movies.*, GenreType, Rating, Platform, DateAdded, UserRating FROM Movies LEFT JOIN Genres ON (Movies.MovieId = Genres.MovieId) LEFT JOIN Ratings ON (Movies.MovieId = Ratings.MovieId) LEFT JOIN StreamingService ON (StreamingService.MovieId= Movies.MovieId) LEFT JOIN Recommendations ON (Recommendations.MovieId= Movies.MovieId) WHERE UserRating = %s AND Movies.DeletedAt IS NULL;""",
                (search_string,))
            result = cursor.fetchall()
            if cursor.rowcount == 0:
                flash('No results found!')
                return redirect('/index')
            else:
                return render_template('complete_movie_search_results.html', result=result,
                                       content_type='application/json')
        else:
            cursor.execute("SELECT Movies.*, GenreType, Rating, Platform, DateAdded, UserRating FROM Movies LEFT JOIN Genres ON (Movies.MovieId = Genres.MovieId) LEFT JOIN Ratings ON (Movies.MovieId = Ratings.MovieId) LEFT JOIN StreamingService ON (StreamingService.MovieId= Movies.MovieId) LEFT JOIN Recommendations ON (Recommendations.MovieId= Movies.MovieId) WHERE Category IN ({}) AND Platform IN ({}) AND Rating IN ({}) AND "
                           "(GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s OR GenreType LIKE %s) AND (Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s"
                           "OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s"
                           "OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s OR Country LIKE %s)".format(
                   str(categories)[1:-1], str(platforms)[1:-1], str(entered_ratings)[1:-1]), (genre_list[0], genre_list[1], genre_list[2], genre_list[3], genre_list[4],genre_list[5], genre_list[6], genre_list[7], genre_list[8], genre_list[9], genre_list[10],
                                                                                              genre_list[11], genre_list[12], countries_list[0], countries_list[1], countries_list[2], countries_list[3], countries_list[4],
                                                                                              countries_list[5], countries_list[6], countries_list[7], countries_list[8], countries_list[9],
                                                                                              countries_list[10], countries_list[11], countries_list[12], countries_list[13], countries_list[14],
                                                                                              countries_list[15],countries_list[16],countries_list[17],countries_list[18],countries_list[19],countries_list[20],
                                                                                              countries_list[21],countries_list[22],countries_list[23],countries_list[24],countries_list[25],countries_list[26],
                                                                                              countries_list[27],countries_list[28],countries_list[29],countries_list[30],countries_list[31],countries_list[32],
                                                                                              countries_list[33],countries_list[34],countries_list[35],countries_list[36],countries_list[37],countries_list[38],
                                                                                              countries_list[39],countries_list[40],countries_list[41],))


            result = cursor.fetchall()

            if cursor.rowcount == 0:
                flash('No results found!')
                return redirect('/index')
            else:
                return render_template('complete_movie_search_results.html', result=result, content_type='application/json')

    else:
        return render_template('filter_index.html', form=form)

###SUGGESTIONS
###Looks at the top 3 tv-ratings for the user's highest user ratings and the top 5 genres for the user's highest user ratings
###gives info about 10 movies based on these values (makes sure that the user has not rated them so it can be updated as the user enters more ratings)
@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    cursor.execute(
        "SELECT Rating, MAX(UserRating) FROM Ratings INNER JOIN Recommendations ON (Recommendations.MovieId= Ratings.MovieId) GROUP BY Rating ORDER BY MAX(UserRating) DESC LIMIT 3")
    list_ratings = [x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT GenreType, MAX(UserRating) FROM Genres INNER JOIN Recommendations ON (Recommendations.MovieId= Genres.MovieId) GROUP BY GenreType ORDER BY MAX(UserRating) DESC LIMIT 5")
    list = [x[0] for x in cursor.fetchall()]

    split_list = [i.split(',', 1)[0] for i in list]

    new_list = []


    for i in range(len(split_list)):
        next_list = '%' + split_list[i] + '%'
        new_list.append(next_list)

    # print(new_list[0])
    cursor.execute(
        "SELECT Movies.*, GenreType, Rating, Platform, DateAdded, UserRating FROM Ratings INNER JOIN Movies ON (Movies.MovieId= Ratings.MovieId) LEFT JOIN Genres ON (Movies.MovieId = Genres.MovieId) LEFT JOIN StreamingService ON (StreamingService.MovieId= Movies.MovieId)LEFT JOIN Recommendations ON (Recommendations.MovieId= Movies.MovieId) WHERE Rating IN ({}) AND (GenreType LIKE %s OR GenreType LIKE %s  OR GenreType LIKE %s  OR GenreType LIKE %s OR GenreType LIKE %s) AND UserRating IS NULL LIMIT 10".format(str(list_ratings)[1:-1]), (new_list[0], new_list[1], new_list[2], new_list[3], new_list[4],))
    result = cursor.fetchall()

    return render_template('complete_movie_search_results.html', result=result, content_type='application/json')

# Main method
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)), debug=True)