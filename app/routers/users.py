from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, db_utils
from app.oauth2 import get_current_user
from app.database import get_db


router = APIRouter(prefix='/users', tags=['Users'])


# Get user
@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    return db_utils.db_get_user_or_404(id, db)


# Create user
@router.post('/', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    return db_utils.db_create_user(db, user)


# Delete user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return db_utils.db_delete_user(db, id, current_user)
