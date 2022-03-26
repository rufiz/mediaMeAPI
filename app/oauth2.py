from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from datetime import datetime, timedelta

from app import schemas, utils, models, db_utils
from app.database import get_db
from app.config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials.',
    headers={'WWW-Authenticate': 'Bearer'}
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, form_data, credentials_exception=credentials_exception):
    '''Checks if the user exists and if the passwords match. If both conditions are met, returns the user.'''
    user = db.query(models.User).filter_by(email=form_data.username).first()
    # Check if the user exists
    if not user:
        raise credentials_exception
    # Check if the passwords match
    if not utils.verify_password(form_data.password, user.password):
        raise credentials_exception
    return user


def verify_access_token(token: str, credentials_exception=credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = verify_access_token(token)
    user = db_utils.db_get_user_or_404(token.id, db)
    return user.id
