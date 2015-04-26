# This is the controller for the interactive database
# imports
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import url_for
from flask import redirect
from flask import g

import sqlite3
from functools import wraps

# configuration
DATABASE = 'soccer.db'
USERNAME = 'admin'
PASSWORD = 'hard_to_guess'
SECRET_KEY = 'p\xffw\x1f\xda\xfe\x16\xfe\xa9\xdf\xfe4\xc0d-f\xaa\xad\xd3^\xcfZH"'

app = Flask(__name__)

# pull in configurations by looking for UPPERCASE variables
app.config.from_object(__name__)

# function used for connecting to the db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# login_required decorator
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# login function
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

# main function
@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM soccer_stats')
    posts = [dict(season=row[0], player=row[1], club=row[2], competition=row[3], goals=row[4], assists=row[5]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

# add post function
@app.route('/add', methods=['POST'])
@login_required
def add():
    season = request.form['season']
    player = request.form['player']
    club = request.form['club']
    competition = request.form['competition']
    goals = request.form['goals']
    assists = request.form['assists']
    if not season or not player or not club or not competition or not goals or not assists:
        flash("All fields are required to add a new entry. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('INSERT INTO soccer_stats (season, player, club, competition, goals, assists) VALUES (?,?,?,?,?,?)', [season, player, club, competition, goals, assists])
        g.db.commit()
        g.db.close()
        flash('New entry was successfully added!')
        return redirect(url_for('main'))   

# logout function
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

