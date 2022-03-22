from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, db_utils
from app.oauth2 import get_current_user
from app.database import get_db


router = APIRouter(prefix='/comments',
                   tags=['Comments'])


@router.post('/', response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.CommentDB, db: Session = Depends(get_db),
                   current_user: int = Depends(get_current_user)):
    return db_utils.db_create_comment(db, comment, current_user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(db: Session = Depends(get_db), comment: schemas.CommentOut = Depends(db_utils.db_get_comment_or_404),
                   current_user: int = Depends(get_current_user)):
    db_utils.db_delete_comment(db, comment, current_user)


# TODO: Add functionality: Users can update their comments
