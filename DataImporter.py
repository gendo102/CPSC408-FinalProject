import sys
import csv
from datetime import datetime

# Database details
import mysql.connector

db = mysql.connector.connect(
    host="34.83.8.98",
    user="root",
    passwd="INSERT DB DETAILS HERE",
    database="FinalProject"
)

# Import data from csv into normalized database
def dataImporter(filename):
    with open(filename + ".csv", "r", encoding='latin1') as csv_data:
        reader = csv.reader(csv_data)
        next(reader)
        for row in reader:
            mycursor = db.cursor()

            # Movies
            mycursor.execute("INSERT INTO Movies(Category,Title,Country,ReleaseYear,Duration,Description)"
                             "VALUES(%s,%s,%s,%s,%s,%s);", (row[2],row[3],row[10],row[12],row[14],row[16],))
            MovieId = mycursor.lastrowid
            db.commit()
            print('Committed to Movies')

            # Actors
            mycursor.execute("INSERT INTO Actors(ActorName,Gender,Age)"
                             "VALUES(%s,%s,%s);", (row[7],row[8],row[9],))
            db.commit()
            print('Committed to Actors')

            # Directors
            mycursor.execute("INSERT INTO Directors(DirectorName,Gender,Age)"
                             "VALUES(%s,%s,%s);", (row[4],row[5],row[6],))
            db.commit()
            print('Committed to Directors')

            # Genres
            mycursor.execute("INSERT INTO Genres(MovieId, GenreType)"
                             "VALUES(%s,%s);", (MovieId,row[15],))
            db.commit()
            print('Committed to Genres')

            # Ratings
            mycursor.execute("INSERT INTO Ratings(MovieId, Rating)"
                             "VALUES(%s,%s);", (MovieId,row[13],))
            db.commit()
            print('Committed to Ratings')

            # Recommendations table is empty upon starting
            # User will input ratings later

            # StreamingService
            mycursor.execute("INSERT INTO StreamingService(MovieId, Platform, DateAdded)"
                             "VALUES(%s,%s,%s);", (MovieId,row[1],datetime.strptime(row[11],'%d-%b-%y'),))
            db.commit()
            print('Committed to StreamingService')

    db.commit()
    db.close()
    print("\nData imported to database!\n")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        dataImporter(filename)
    else:
        print('Enter filename as command line parameter. Ex: python DataImporter.py test')