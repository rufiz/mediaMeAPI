from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from sqlalchemy.orm import Session

from passlib.hash import pbkdf2_sha256

from app import models, schemas
from app.database import get_db


# Extract all the posts
def db_get_posts(
    limit: int = None, offset: int = None, db: Session = Depends(get_db)
):
    return db.query(models.Post).limit(limit).offset(offset).all()


# Extract a post with an id
def db_get_post_or_404(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=id).first()
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Post with id: {id} does not exist.')
    return post


# Create a post
def db_create_post(db: Session, post: schemas.PostDB, user_id: int):
    user = db_get_user_or_404(user_id, db)
    new_post = models.Post(**post.dict(), user_id=user_id, user=user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Update a post
def db_update_post(db: Session, post: schemas.PostPartialUpdate, id: int, current_user: int):
    post_to_update = db.query(models.Post).filter_by(id=id)
    if not post_to_update:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID: {id} does not exist.')

    if post_to_update.first().user_id != current_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized action.'
        )
    post_to_update.update(post.dict(exclude_unset=True),
                          synchronize_session=False)
    db.commit()
    return post_to_update.first()


# Delete post
def db_delete_post(db: Session, post: schemas.PostOut, current_user: int):
    # There is no need for error handling here since db_get_post_or_404
    # handles the 404 post not found error.
    if post.user_id != current_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized action.'
        )
    db.delete(post)
    db.commit()


# Extract a comment with an id
def db_get_comment_or_404(id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter_by(id=id).first()
    if not comment:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Comment with id: {id} does not exist.')
    return comment


# Create comment
def db_create_comment(db: Session, comment: schemas.CommentDB, user_id: int):
    post = db_get_post_or_404(comment.post_id, db)
    new_comment = models.Comment(**comment.dict(), user_id=user_id, post=post)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# Delete comment
def db_delete_comment(db: Session, comment: schemas.CommentOut, current_user: int):
    # db_get_comment_or_404 is injected as a Dependancy to /comments delete route
    # and it takes care of 404 not found error.
    # Compare the user_id from comment and current_user raise credentials error
    # if they do not match.
    if comment.user_id != current_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized action.'
        )

    db.delete(comment)
    db.commit()


# Get user
def db_get_user_or_404(id: int, db: Session):
    user = db.query(models.User).filter_by(id=id).first()
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'No user with id {id} found.')
    return user


# Create user
def db_create_user(db: Session, user: schemas.UserIn):
    user_exists = db.query(models.User).filter_by(email=user.email).first()
    if user_exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f'A user with email:{user.email} already exists.'
        )

    user.password = pbkdf2_sha256.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Delete user
def db_delete_user(db: Session, id: int, current_user: int):
    # There is no need for error handling here since db_get_post_or_404
    # handles the 404 post not found error.
    user = db_get_user_or_404(id, db)
    if user.id != current_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized action.'
        )
    db.delete(user)
    db.commit()
