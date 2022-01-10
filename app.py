from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'dbms_mini_pro'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'dbmspros'
app.config['MYSQL_PASSWORD'] = 'Br!ght3n'
app.config['MYSQL_DB'] = 'movie_manage'


mysql = MySQL(app)


@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    rows = cursor.execute(
        'SELECT * FROM movie_manage.movies_list order by name asc')
    if rows > 0:
        details = cursor.fetchall()
        cursor.connection.commit()
        cursor.close()
        return render_template('viewlist.html', details=details, status=["active", "", "", "", ""])


@app.route('/addmovies', methods=['POST', 'GET'])
def addmovies():

    if request.method == 'POST':
        """ detail = request.form
        print(detail) """
        name = request.form['mname']
        director = request.form['dname']
        language = request.form['languauge']
        yor = request.form['yor']
        genre = request.form['genre']
        rate = request.form['rating']
        ranking = request.form['ranking']
        imdb = request.form['imdb']
        timedur = request.form['runtime']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT into movies_list(name,language,year_of_release,genre,rating,ranking,imdb,runtime,director) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, language, yor, genre, rate, ranking, imdb, timedur, director))

        row = cursor.execute('SELECT * FROM movies_list')

        print("query Executed")
        if row > 0:
            detail = cursor.fetchall()
            cursor.connection.commit()
            cursor.close()
            return render_template('add.html', msg="Added Successfully", color='success', status=["", "active", "", "", ""])
    return render_template('add.html', status=["", "active", "", "", ""])


@app.route('/searchmovies', methods=['POST', 'GET'])
def search_movies():

    if request.method == 'POST':
        movname = request.form['mname']
        cursor = mysql.connection.cursor()
        row = cursor.execute(
            'SELECT * FROM movies_list WHERE name=%s', [movname])
        if row > 0:
            detail = cursor.fetchall()
            cursor.connection.commit()
            cursor.close()
            print(detail)
            return render_template('update.html', status=["", "", "active", "", ""], results=detail)
        msg = "Movie not found!"
        return render_template('update.html', status=["", "", "active", "", ""], color='warning', message=msg)

    return render_template('update.html', status=["", "", "active", "", ""])


@app.route('/updatemovies', methods=['GET', 'POST'])
def update_movies():
    if request.method == 'POST':
        movname = request.form['mname']
        director = request.form['dname']
        language = request.form['languauge']
        yor = request.form['yor']
        genre = request.form['genre']
        rate = request.form['rating']
        ranking = request.form['ranking']
        imdb = request.form['imdb']
        timedur = request.form['runtime']

        cursor = mysql.connection.cursor()
        row = cursor.execute(
            'SELECT * FROM movies_list WHERE name=%s', [movname])
        if row > 0:
            detail = cursor.fetchall()
            cursor.execute(
                'UPDATE movies_list SET language=%s,year_of_release=%s,genre=%s,rating=%s,ranking=%s,imdb=%s,runtime=%s,director=%s WHERE name=%s',
                [language, yor, genre, rate, ranking, imdb, timedur, director, movname])
            updates = cursor.execute('SELECT * FROM movies_list')
            if updates > 0:
                detail = cursor.fetchall()
            cursor.connection.commit()
            cursor.close()
            msg = "Updated Successfully!"
            print(detail)
            return render_template('update.html', status=["", "", "active", "", ""], color='success', message=msg)
        msg = "Update Failed!"
        return render_template('update.html', status=["", "", "active", "", ""], color='danger', message=msg)
    return render_template('update.html', status=["", "", "active", "", ""])


@app.route('/searchdelmovies', methods=['POST', 'GET'])
def search_del_movies():

    if request.method == 'POST':
        movname = request.form['mname']
        cursor = mysql.connection.cursor()
        row = cursor.execute(
            'SELECT * FROM movies_list WHERE name=%s', [movname])
        if row > 0:
            detail = cursor.fetchall()
            cursor.connection.commit()
            cursor.close()
            print(detail)
            return render_template('delete.html', status=["", "", "", "active", ""], results=detail)
        msg = "Movie not found!"
        return render_template('delete.html', status=["", "", "", "active", ""], color='warning', message=msg)

    return render_template('delete.html', status=["", "", "", "active", ""])


@ app.route('/deletemovies', methods=['POST', 'GET'])
def delete_movies():
    if request.method == 'POST':
        movname = request.form['mname']
        director = request.form['dname']
        language = request.form['languauge']
        yor = request.form['yor']
        genre = request.form['genre']
        rate = request.form['rating']
        ranking = request.form['ranking']
        imdb = request.form['imdb']
        timedur = request.form['runtime']

        cursor = mysql.connection.cursor()
        print("connection Set")
        row = cursor.execute(
            'SELECT * FROM movies_list WHERE name=%s', [movname])
        print('Query Executed')
        if row > 0:
            detail = cursor.fetchall()
            cursor.execute(
                'DELETE FROM movies_list WHERE name=%s', [movname])
            updates = cursor.execute('SELECT * FROM movies_list')
            if updates > 0:
                detail = cursor.fetchall()
            cursor.connection.commit()
            cursor.close()
            msg = "Deleted Successfully!"
            print(detail)
            return render_template('delete.html', status=["", "", "", "active", ""], color='success', message=msg)
        msg = "Delete Failed!"
        return render_template('delete.html', status=["", "", "", "active", ""], color='danger', message=msg)
    return render_template('delete.html', status=["", "", "", "active", ""])


@ app.route('/about')
def about():
    return render_template('about.html', status=["", "", "", "", "active"])


if __name__ == '__main__':
    app.run(debug=True)
