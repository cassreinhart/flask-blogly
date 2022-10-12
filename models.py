"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
#run SQLAlchemy, whatever is returned will be stored in db var

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """create a new user"""

    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    image_url = db.Column(db.String, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnSHPlV1tN5yuFqgNWuEu02d8mxiESub2jGA&usqp=CAU')
