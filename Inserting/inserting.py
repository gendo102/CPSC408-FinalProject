from flask import Flask, render_template, request, redirect, flash, url_for
import os
import pymysql
from wtforms import Form, StringField, SelectField
import datetime

app = Flask(__name__, template_folder="Templates")

app.secret_key = '701701'
conn = pymysql.connect("34.83.209.196","root","Ktggym98","FINALPROJECT")
cursor = conn.cursor()


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
                     ('Sport', 'Sport'), ]
    add_genre = SelectField('Genres', choices=choices_genre)
    choices_rating = [('Choose selection:', 'Choose selection:'),
                      ('TV-Y7', 'TV-Y7'),
                      ('TV-G', 'TV-G'),
                      ('TV-PG', 'TV-PG'),
                      ('TV-MA', 'TV-MA'),
                      ('PG-13', 'PG-13'),
                      ('TV-14', 'TV-14'),
                      ('R', 'R'),
                      ('Not Rated', 'Not Rated'),
                      ('Approved', 'Approved'), ]
    add_rating = SelectField('Ratings', choices=choices_rating)
    platform_choices = [('Choose selection:', 'Choose selection:'),
                        ('Netflix', 'Netflix'),
                        ('DisneyPlus', 'DisneyPlus'), ]
    add_platform = SelectField("Platforms", choices=platform_choices, default=None)



@app.route('/', methods=['GET', 'POST'])
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
            cursor.execute("""SELECT *  FROM Recommendations WHERE MovieID IN(SELECT MovieID
                                                                           FROM Movies
                                                                           WHERE Title = %s);""", (title,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Recommendation already exists!')
                #can add to redirect to update
                return redirect('/')
            else:
                cursor.execute("""INSERT INTO Recommendations(UserRating,MovieId)
                                      SELECT %s, MovieId FROM Movies WHERE Title = %s;""", (user_rating, title,))
                conn.commit()
                flash("Recommendation Record Inserted Successfully")
                return redirect('/')

        elif search.data['add_table'] == 'Actor':
            actor_name = request.form['add_actor_name']
            actor_age = request.form['add_actor_age']
            actor_gender = search.data['add_gender_actor']
            cursor.execute("""SELECT *  FROM Actors WHERE ActorName = %s;""", (actor_name,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Actor already exists!')
                return redirect('/')
            else:
                cursor.execute("""INSERT INTO Actors(ActorName,Age, Gender)
                                      VALUES (%s, %s, %s);""", (actor_name, actor_age, actor_gender,))
                conn.commit()
                flash("Actor Record Inserted Successfully")
                return redirect('/')

        elif search.data['add_table'] == 'Director':
            director_name = request.form['add_director_name']
            director_age = request.form['add_director_age']
            director_gender = search.data['add_gender_director']
            cursor.execute("""SELECT *  FROM Directors WHERE DirectorName = %s;""", (director_name,))
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                flash('Director already exists!')
                return redirect('/')
            else:
                cursor.execute("""INSERT INTO Directors(DirectorName, Age, Gender)
                                      VALUES (%s, %s, %s);""", (director_name, director_age, director_gender,))
                conn.commit()
                flash("Director Record Inserted Successfully")
                return redirect('/')

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
            return redirect('/')



