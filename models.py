"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
#run SQLAlchemy, whatever is returned will be stored in db var

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """create a new user"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable= False, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnSHPlV1tN5yuFqgNWuEu02d8mxiESub2jGA&usqp=CAU')

    posts = db.relationship("Post", backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"

class Post(db.Model):
    """create user blog post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary="posts_tags", backref="posts") #adds "through" relationship

    @property
    def readable_date(self):
        """return formatted date"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    
    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.user_id}>"

class Tag(db.Model):
    """A tag for posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"

class PostTag(db.Model):
    """Map a tag to a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    