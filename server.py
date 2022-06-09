"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """view homepage"""

    return render_template('homepage.html')

@app.route('/movies')
def get_all_movies():
    """View all movies."""

    movies = crud.get_all_movies()

    return render_template("all_movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


@app.route('/movies/<movie_id>/ratings', methods=["POST"])
def create_rating(movie_id):
    """Create a rating for a movie"""
    # get id from session to check for login
    # if not logged in some message about logging in
    # get request from form for rating
    # create rating and add and commit
    
    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash ("You must log in to rate a movie")
    elif not rating_score:
        flash ("You did not select a rating")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash (f'You rated this movie {rating_score} out of 5')
    
    return redirect(f"/movies/{movie_id}")




@app.route('/users')
def get_all_users():
    """View all users"""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show one user info"""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)
    

@app.route('/users', methods=["POST"])
def register_user():
    """create a new user"""

    email = request.form.get("email") #form email
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user:
        flash(f'Cannot create an account with that e-mail') 
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created please log in')
    return redirect('/')
    

@app.route('/login', methods=["POST"])
def login_user():

    email = request.form.get("email") #form email
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user.password != password:
        flash('email or password does not match')
    else:
        session["user_email"] = user.email
        flash('Logged in')
    return redirect('/')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
