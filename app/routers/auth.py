from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, oauth2
from app.database import get_db


router = APIRouter(prefix='/login', tags=['Login'])


@router.post('/', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = oauth2.authenticate_user(db, form_data)
    access_token = oauth2.create_access_token({'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
