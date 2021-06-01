from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, sql

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String(250), nullable=False, default="empty")


    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<User id: {self.id} - {self.first_name} {self.last_name}>'


class Post(db.Model):

    __tablename__= 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(125), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user =  db.relationship('User', backref = 'posts')

    post_tag = db.relationship('PostTag', backref = 'post')

    def __repr__(self):
        return f'<Post id: {self.id} - created date {self.created_at} by the user: {self.user}>'

    
class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(125), nullable=False, unique=True)

    post_tag = db.relationship('PostTag', backref = 'tag')



class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)