"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def show_home():
    """show home page"""
    users = User.query.all()

    return render_template('user.html', users=users)

@app.route('/users')
def show_all_users():
    """Show all users"""
    users = User.query.all();
    return render_template('user.html', users=users)

@app.route('/users/new')
def show_add_user_form():
    """Show form to add a new user"""

    return render_template('create.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Create a new user instance, redirect to user list"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users")

@app.route('users/<int: user_id>')
def show_user_detail():
    """Show user details for a single user"""

    user = User.query.get_or_404(user_id)
    return render_template("info.html", user=user)