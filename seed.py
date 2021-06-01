from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add users
first_user = User(first_name='Tom', last_name='Smith', image_url='https://i.pinimg.com/originals/92/a6/2f/92a62f0221f58fe503a15fcb13f5c107.png')
second_user = User(first_name='Jack', last_name='Sparrow', image_url='https://iadsb.tmgrup.com.tr/0999d9/0/0/0/0/2048/1199?u=https://idsb.tmgrup.com.tr/2017/03/19/jack-sparrow-might-be-inspired-by-a-muslim-captain-1489951367309.jpg')

# Add posts
post_1 = Post(title='First title', content='This text of the fisrt post', user_id=1)
post_2 = Post(title='Second title', content='This text of the second post', user_id=2)
post_3 = Post(title='Third title', content='This text of the third post', user_id=1)

#Add tags
tag_1 = Tag(name='info')
tag_2 = Tag(name='main')


#Add posts_tags
posttag_1 = PostTag(post_id=1, tag_id=2)
posttag_2 = PostTag(post_id=2, tag_id=1)
posttag_3 = PostTag(post_id=3, tag_id=2)

# Add new objects to session, so they'll persist
# Commit--otherwise, this never gets saved!

db.session.add_all([first_user, second_user])
db.session.commit()


db.session.add_all([post_1, post_2, post_3])
db.session.commit()


db.session.add_all([tag_1, tag_2])
db.session.commit()


db.session.add_all([posttag_1, posttag_2, posttag_3])
db.session.commit()