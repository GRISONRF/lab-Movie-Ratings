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

    email1 = request.form.get("email") #form email
    password = request.form.get("password")
    # email1 - data
    # email2 - form
    user = crud.get_users()
    
    # for item in crud.get_users: #<email="asdasdsa@" passowrd='asdasd>
    if user.email == email1:
        flash(f'Cannot create an account with that e-mail') 
    else:
        user = crud.create_user(email1, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created please log in')
        return redirect('/')
    
    return render_template("user_details.html", item=item, user=user)



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
