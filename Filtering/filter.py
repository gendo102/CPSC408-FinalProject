from flask import Flask, render_template, request, redirect, flash, url_for
import os
import pymysql
from wtforms import Form, StringField, SelectField
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField

app = Flask(__name__, template_folder="templates")
app.secret_key = '701701'
conn = pymysql.connect("34.83.209.196","root","Ktggym98","FINALPROJECT")
cursor = conn.cursor()


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

@app.route('/', methods=['GET', 'POST'])
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
            return redirect('/')
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
            return redirect('/')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['select_filter'] == 'Category':
        search_string = "%" + request.form['select_category'] + "%"
        cursor.execute("""SELECT *  FROM Movies WHERE Category LIKE %s AND DeletedAt IS NULL 
                                                                          ORDER BY Title;""", (search_string,))

        result = cursor.fetchall()

        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/')
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
            return redirect('/')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Title':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Movies WHERE Title LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Year':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Movies WHERE ReleaseYear LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Actor':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Actors WHERE ActorName LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('person_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Director':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Directors WHERE DirectorName LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('person_search_results.html', result=result, content_type='application/json')

    elif search.data['search_options'] == 'Country':
        search_string = "%" + request.form['search_field'] + "%"
        cursor.execute("""SELECT * FROM Movies WHERE Country LIKE %s;""", (search_string,))
        result = cursor.fetchall()
        if cursor.rowcount == 0:
            flash('No results found!')
            return redirect('/')
        else:
            return render_template('movie_search_results.html', result=result, content_type='application/json')

    else:
        flash('No results found!')
        return redirect('/')
