from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routers import posts, comments, auth, users


origins = ['*']

app = FastAPI()
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup():
    Base.metadata.create_all(bind=engine)


@app.get('/', tags=['Home Page'])
async def home_page():
    return {'message': 'up and running.'}
