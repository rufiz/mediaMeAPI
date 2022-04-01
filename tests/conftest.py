from asgi_lifespan import LifespanManager
import httpx
import pytest
import asyncio

from app.schemas import UserIn
from app.main import app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


# Creates a test client from your FastAPI application
@pytest.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url='http://127.0.0.1:8000') as test_client:
            yield test_client


# Creates a test user, signs in with the user, returns a token and then deletes it from the database
@pytest.fixture
async def test_access_token(test_client: httpx.AsyncClient):
    payload = UserIn(email='client_test@gm.com',
                     password='test_password').dict()  # Create a user info
    # Create a user in db
    new_user = await test_client.post('/users/', json=payload)
    # Extract returning information. Note: refer to schemas
    new_user_response = new_user.json()
    new_user_login_data = {'username': new_user_response.get('email'),
                           'password': payload.get('password')}
    # Login and receive the access token
    access_token = await test_client.post('/login/', data=new_user_login_data)
    yield access_token.json()  # Return access token to the test function
    # Delete the test user from the database
    await test_client.delete(f'/users/{new_user_response.get("id")}',
                             headers={'Authorization': f'Bearer {access_token.json().get("access_token")}',
                                      'typ': 'JWT'})
