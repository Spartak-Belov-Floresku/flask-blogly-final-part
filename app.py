from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:password@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = 'hello'
app.debug = True
DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """List all users"""

    return redirect('/users')


@app.route('/users')
def list_users():
    """List all users"""

    users = User.query.all()
    return render_template('list_users.html', users = users)


@app.route('/users/new')
def add_form_user():
    """Show form to create a new user"""

    return render_template('form_user.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """Add a new user to the database"""

    """get data from POST request"""
    first_name = request.form.get('first_name', 'empty')
    last_name = request.form.get('last_name', 'empty')
    img_url = request.form.get('img_url', 'empty')

    """create User object"""
    user = User(first_name=first_name, last_name=last_name, image_url=img_url)

    """Add new objects to session, so they'll persist"""
    db.session.add(user)

    """Commit--otherwise, this never gets saved!"""
    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:id>")
def data_user(id):
    """Show a user page"""

    """Get user from db"""
    user = User.query.get(id)

    """get all related posts to the users"""
    posts = user.posts

    return render_template('user.html', user=user, posts = posts)


@app.route('/users/<int:id>/edit')
def edit_form(id):
    """Show an edit user form"""

    """Get user from db"""
    user = User.query.get(id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:id>/edit', methods=['POST'])
def edit_user(id):
    """Update user data"""

    """get user from db"""
    user = User.query.get(id)

    """get data from form"""
    first_name = request.form.get('first_name', 'empty')
    last_name = request.form.get('last_name', 'empty')
    image_url = request.form.get('img_url', 'empty')

    """update user data"""
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()


    return redirect('/users')


@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):

    """Delete user data from database"""

    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/users')




@app.route('/users/<int:id>/posts/new')
def add_form_post(id):

    """Show form to add a post for that user"""
    user = User.query.get(id)
    tags = Tag.query.all()

    return render_template('form_post.html', user=user, tags=tags)


@app.route('/users/<int:id>/posts/new', methods=['POST'])
def add_user_post(id):
    """Handle add form; add post and redirect to the user detail page"""

    """get data from form"""
    title = request.form.get('title', 'empty')
    content = request.form.get('content', 'empty')

    """Create a new post"""
    post = Post(title=title, content=content, user_id = id)

    db.session.add(post)
    db.session.commit()

    """get list of check boxs"""
    tags = request.form.getlist('tags')

    if len(tags):

        tags_ids = []
        """
        retrieving all tags name from post request,
        process them to get their ids from db
        """
        for tag in tags:
            tag_obj = Tag.query.filter_by(name=tag).first()
            tags_ids.append(tag_obj.id)

        posts_tags = []
        """
        creating PostTag objects with related 
        tag's and post's ids, save them into db
        """
        for t_id in tags_ids:
            posts_tags.append(PostTag(post_id=post.id, tag_id=t_id))
        
        db.session.add_all(posts_tags)
        db.session.commit()

    return redirect(f'/users/{id}')


@app.route('/posts/<int:id>')
def show_post(id):
    """Show a post."""

    """get a post from posts table"""
    post = Post.query.get(id)

    """getting ref-ids of all tags related to this post"""
    post_tags = post.post_tag

    """run loop to retrive all the tags that are related to the post"""
    tags = [el.tag for el in post_tags]


    return render_template('show_post.html', post=post, tags =tags)


@app.route('/posts/<int:id>/edit')
def edit_post_form(id):
    """Show form to edit a post, and to cancel (back to user page)"""

    """Get post from db"""
    post = Post.query.get(id)

    """retrieving all post's rows from posts_tags table"""
    post_tag_rows = post.post_tag

    """retrieving all tag's ids that relative to the post"""
    tags_ids = []
    if len(post_tag_rows):
        for row in post_tag_rows:
            tags_ids.append(row.tag_id)

    """retrieving all tags from db"""
    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags_ids=tags_ids, tags=tags)


@app.route('/posts/<int:id>/edit', methods=['POST'])
def edit_user_post(id):
    """Handle editing of a post. Redirect back to the post view."""

    """get post from db"""
    post = Post.query.get(id)

    """get data from form"""
    title = request.form.get('title', 'empty')
    content = request.form.get('content', 'empty')

    """update post data"""
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    """check if post has record into posts_tags table"""
    if len(post.post_tag):

        """delete all rows related to the post in the posts_tags table"""
        all_posts_tags = PostTag.query.filter_by(post_id=id).all()
        for post_tag in all_posts_tags:
            db.session.delete(post_tag)
        db.session.commit()

    """get list of check boxs"""
    tags = request.form.getlist('tags')

    if len(tags):

        tags_ids = []
        """
        retrieving all tags name from post request,
        process them to get their ids from db
        """
        for tag in tags:
            tag_obj = Tag.query.filter_by(name=tag).first()
            tags_ids.append(tag_obj.id)

        posts_tags = []
        """
        creating PostTag objects with related 
        tag's and post's ids, save them into db
        """
        for t_id in tags_ids:
            posts_tags.append(PostTag(post_id=id, tag_id=t_id))
        
        db.session.add_all(posts_tags)
        db.session.commit()

    return redirect(f'/posts/{id}')


@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):

    """Delete the post."""
    post = Post.query.get(id)
    user_id = post.user_id


    """check if post has record into posts_tags table"""
    if len(post.post_tag):
        
        """delete all rows related to the post in the posts_tags table"""
        all_posts_tags = PostTag.query.filter_by(post_id=id).all()
        for post_tag in all_posts_tags:
            db.session.delete(post_tag)
        db.session.commit()
    
    """delete the post from data base"""
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/tags')
def tags_lists():
    """Lists all tags, with links to the tag detail page"""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:id>')
def show_tag(id):
    """Show detail about a tag. Have links to edit form and to delete"""

    tag = Tag.query.get(id)

    """getting ref-id of all posts related to this tag"""
    posts_tag = tag.post_tag

    """run loop to obtain all the post titles that are related to the tag"""
    posts = [el.post for el in posts_tag]

    return render_template('show_tag.html', tag=tag, posts=posts)


@app.route('/tags/new')
def tag_add_form():

    """Shows a form to add a new tag"""

    return render_template('form_tag.html')


@app.route('/tags/new', methods=['POST'])
def add_new_tag():

    """Process add form, adds tag, and redirect to tag list"""

    """get data from form"""
    name = request.form.get('name', 'empty')

    """Create a new post"""
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()


    return redirect('/tags')


@app.route('/tags/<int:id>/edit')
def edit_tag_form(id):
    """Show edit form for a tag."""

    """Get post from db"""
    tag = Tag.query.get(id)

    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:id>/edit', methods=['POST'])
def edit_tag_post(id):
    """Process edit form, edit tag, and redirects to the tags list"""

    """get tag from db"""
    tag = Tag.query.get(id)

    """get data from form"""
    name = request.form.get('name', 'empty')

    """update post data"""
    tag.name = name

    db.session.add(tag)
    db.session.commit()


    return redirect('/tags')



@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):

    """Delete a tag"""
    tag = Tag.query.get(id)

    """check if tag has record into posts_tags table"""
    if len(tag.post_tag):
        
        """delete all rows related to the tag in the posts_tags table"""
        all_posts_tags = PostTag.query.filter_by(tag_id=id).all()
        for tag in all_posts_tags:
            db.session.delete(tag)
        db.session.commit()
    
    """delete tag from tags table"""
    Tag.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/tags')




if __name__ == "__main__":
    app.run(debug=True)

