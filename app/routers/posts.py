from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import get_current_user
from app import schemas, db_utils, models


router = APIRouter(
    prefix='/posts', tags=['Posts'])


# Extract all the posts
@router.get('/', response_model=List[schemas.PostOut])
async def get_posts(posts: List[schemas.PostOut] = Depends(db_utils.db_get_posts)):
    return posts


# Extract a post with an id
@router.get('/{id}', response_model=schemas.PostOut)
async def get_post(post: schemas.PostOut = Depends(db_utils.db_get_post_or_404)):
    return post


# Create a post
@router.post('/', response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostDB, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return db_utils.db_create_post(db, post, current_user)


# Update a post
@router.put('/{id}', response_model=schemas.PostOut)
async def update_post(post: schemas.PostPartialUpdate, id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(get_current_user)):
    return db_utils.db_update_post(db, post, id, current_user)


# Delete a post
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(db: Session = Depends(get_db), post: schemas.PostOut = Depends(db_utils.db_get_post_or_404),
                      current_user: int = Depends(get_current_user)):
    db_utils.db_delete_post(db, post, current_user)
