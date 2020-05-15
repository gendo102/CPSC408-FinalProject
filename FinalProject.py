from flask import Flask, render_template, request, redirect, flash, url_for, Response
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

        flash("Record Inserted Successfully")

@app.route('/delete/<string:MovieId>', methods = ['GET'])
def delete(MovieId):
    cursor.execute("UPDATE Movies, SET DeletedAt = current_date WHERE MovieId=%s", (MovieId,))
    conn.commit()
    flash("Record Deleted Successfully")
    return redirect(url_for('Movies'))

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
        flash("Data Updated Successfully")
        conn.commit()
        return redirect(url_for('Movies'))

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

# Main method
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)), debug=True)