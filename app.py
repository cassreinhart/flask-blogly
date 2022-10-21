"""Blogly application."""

from flask import Flask, request, redirect, render_template, current_app
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    """show home page"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('posts/homepage.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """show 404 page"""

    return render_template('404.html'), 404

############## USER ROUTES BELOW ################

@app.route('/users')
def show_all_users():
    """Show all users"""
    users = User.query.order_by(User.first_name, User.last_name).all();
    return render_template('users/index.html', users=users)

@app.route('/users/new')
def show_add_user_form():
    """Show form to add a new user"""

    return render_template('users/create.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Create a new user instance, redirect to user list"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} added!")

    return redirect(f"/users")

@app.route('/users/<int:user_id>')
def show_user_detail(user_id): #We need this here to use the variable from the url
    """Show user details for a single user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/info.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Show edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def post_edited_user(user_id):
    """Process edit form, redirect to Users page"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} updated!")

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Handle form submission to delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.first_name} {user.last_name} deleted!")

    return redirect('/users')


##################### POST ROUTES BELOW ######################

@app.route('/users/<int:user_id>/posts/new')
def posts_add_post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    #not sure if line above will work... name conflict?
    return render_template('posts/create_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def posts_handle_add_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user, 
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"New Post: {new_post.title} added!")

    return redirect('/users/{user_id}}')

@app.route('/posts/<int:post_id>') 
def posts_show_post_details(post_id):
    """Show a post.
    Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all() #get tags from db
    return render_template('posts/edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def posts_handle_edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() # I don't understand this line very well.....

    db.session.add(post)
    db.session.commit()
    flash(f"Post: {post.title} edited!")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def posts_delete(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


##################### TAG ROUTES BELOW ######################

@app.route('/tags')
def list_all_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.order_by('name').all()

    return render_template('tags/list.html', tags=tags)
    
@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/tag.html', tag=tag)

@app.route('/tags/new')
def show_add_tag_form():
    """Shows a form to add a new tag."""
    #Why do I need posts in this route???
    return render_template('/tags/add.html')

@app.route('/tags/new', methods=['POST'])
def handle_add_tag():
    """Process add form, adds tag, and redirect to tag list."""
    
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()
    flash(f"New Tag: {new_tag.name} added!")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('/tags/edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag: {tag.name} edited!")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag {tag.title} deleted.")

    return redirect('/tags')