from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:password@localhost/blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class User_Post_Tag_PostTag_ViewsTestCase(TestCase):
    """Tests for views for "User, Post, Tag, PostTag"""

    def setUp(self):

        """Add sample User, Post, Tag, PostTag"""

        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
        
        user = User(first_name="Tom", last_name="Smith")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='New post', content='Some content', user_id = user.id)
        
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

        tag = Tag(name='info')

        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id

        posttag = PostTag(post_id=post.id, tag_id=tag.id)


        db.session.add(posttag)
        db.session.commit()

        

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    """run test to get all users"""
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tom', html)

    """run test to get user page"""
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4 class="mb-0 mt-0">Tom Smith</h4>', html)

    """run test to create a new user in database"""
    def test_add_user(self):
        with app.test_client() as client:
            user = {'first_name': 'John', 'last_name': 'Smith'}
            resp = client.post('/users/new', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Smith', html)


    """run test to change user's data in database"""
    def test_edit_user(self):
        with app.test_client() as client:
            user = {'first_name': 'Tom', 'last_name': 'Walker'}
            resp = client.post(f'/users/{self.user_id}/edit', data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tom Walker', html)


    """run test to get all postes for user"""
    def test_list_posts_for_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New post', html)

    """run test to get post page"""
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Some content</p>', html)

    
    """run test to create a new post in database"""
    def test_add_post(self):
        with app.test_client() as client:
            post = {'title': 'Secon title', 'content': 'Second content', 'user_id': self.user_id}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Secon title', html)

    """run test to change post's data in database"""
    def test_edit_post(self):
        with app.test_client() as client:
            post = {'title': 'Change post title', 'content': 'Change post content'}
            resp = client.post(f'/posts/{self.post_id}/edit', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Change post title', html)

    """run test to get all tags"""
    def test_list_tags(self):
        with app.test_client() as client:
            resp = client.get('/tags')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('info', html)

    """run test to get tag page"""
    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f'/tags/{self.tag_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('info', html)


    """run test to create a new tag in database"""
    def test_add_tag(self):
        with app.test_client() as client:
            tag = {'name': 'new tag'}
            resp = client.post('/tags/new', data=tag, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('new tag', html)

    """run test to change tag's data in database"""
    def test_edit_tag(self):
        with app.test_client() as client:
            tag = {'name': 'updated tag'}
            resp = client.post(f'/tags/{self.tag_id}/edit', data=tag, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('updated tag', html)

    """run test to get all tag for post"""
    def test_list_tags_for_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('info', html)