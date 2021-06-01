from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:password@localhost/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class User_Post_Tag_PostTag_ModelTestCase(TestCase):
    """Tests for model for User, Post, Tag, PostTag"""

    def setUp(self):
        """Clean up any existing User, Post, Tag, PostTag"""

        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    """run test to ctreate user object"""
    def test_create_user_obj(self):
        user = User(first_name='Tom', last_name='Smith')

        self.assertEqual(user.last_name, "Smith")

    """run test to insert user data into database"""
    def test_insert_user_to_db(self):
        user = User(first_name='Tom', last_name='Smith')
        
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.last_name, 'Smith')

    """run test to ctreate post object"""
    def test_create_post_obj(self):
        post = Post(title='New post', content='Some content', user_id = 1)

        self.assertEqual(post.user_id, 1)


    """run test to insert post data into database"""
    def test_insert_post_to_db(self):

        user = User(first_name='Tom', last_name='Smith')
        
        db.session.add(user)
        db.session.commit()

        post = Post(title='New post', content='Some content', user_id = user.id)
        
        db.session.add(post)
        db.session.commit()

        self.assertEqual(post.user.id, user.id)

    """run test to ctreate Tag and PostTag object and insert into the database"""
    def test_create_PostTag_obj_insert_db(self):
        user = User(first_name='Tom', last_name='Smith')
        
        db.session.add(user)
        db.session.commit()

        post = Post(title='New post', content='Some content', user_id = user.id)
        
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="New tag")

        db.session.add(tag)
        db.session.commit()

        post_tag = PostTag(post_id=post.id, tag_id=tag.id)

        db.session.add(post_tag)
        db.session.commit()

        self.assertEqual(post_tag.post_id, post.id)
        self.assertEqual(post_tag.tag_id, tag.id)