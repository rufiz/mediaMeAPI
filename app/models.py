from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, null
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    publication_date = Column(
        'publication_date', DateTime, nullable=False, server_default='NOW()')
    title = Column('title', String(255), nullable=False)
    content = Column('content', Text(), nullable=False)
    # backref keyword returns the comments as a list when querying the posts table
    comments = relationship('Comment', backref='post')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    post_id = Column('post_id', ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    publication_date = Column(
        'publication_date', DateTime, nullable=False, server_default=text('NOW()'))
    content = Column('content', Text(), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    email = Column('email', String, unique=True, nullable=False)
    password = Column('hashed_password', String, nullable=False)
    created_at = Column('created_at', DateTime,
                        nullable=False, server_default=text('NOW()'))
    # User object needs to be passed as user variable when creating a post
    posts = relationship('Post', backref='user')
