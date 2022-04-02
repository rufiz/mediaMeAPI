import httpx
import pytest

from fastapi import status

from app.schemas import PostDB, PostPartialUpdate


@pytest.mark.asyncio
class TestPosts:
    async def test_get_posts_valid(self, test_client: httpx.AsyncClient):
        # Extract all the posts
        response = await test_client.get('/posts/')
        # Assert it returns 200 status code
        assert response.status_code == status.HTTP_200_OK

    async def test_get_post_valid(self, test_client: httpx.AsyncClient, test_create_post):
        # Create a post and read the response
        response = test_create_post
        response_json = response.json()
        # Get the created post
        extracted_post = await test_client.get(f'/posts/{response_json.get("id")}')
        extracted_post_json = extracted_post.json()
        # Assert if the status code and the content match
        assert extracted_post.status_code == status.HTTP_200_OK
        assert extracted_post_json.get('title') == 'Pytest Fixture'
        assert extracted_post_json.get('content') == 'Created with Pytest'

    async def test_update_post_valid(self, test_client: httpx.AsyncClient, test_create_post, test_access_token):
        # Create a post
        response = test_create_post
        response_json = response.json()
        # Update the created post
        post_to_update = PostPartialUpdate(title='Update with Pytest',
                                           content='Pytest is awesome').dict()
        response_from_update_post = await test_client.put(f'/posts/{response_json.get("id")}', json=post_to_update, headers={'Authorization': f'Bearer {test_access_token.get("access_token")}',
                                                                                                                             'typ': 'JWT'})
        response_from_update_post_json = response_from_update_post.json()
        # Assert the response from the updated post is the same as
        # the response post
        assert response_from_update_post_json.get(
            'title') == post_to_update.get('title')
        assert response_from_update_post_json.get(
            'content') == post_to_update.get('content')


@pytest.fixture
async def test_create_post(test_client: httpx.AsyncClient, test_access_token):
    # Create the payload with PostDB schema
    payload = PostDB(title='Pytest Fixture',
                     content='Created with Pytest').dict()
    # Post it to the /posts/ endpoint
    response = await test_client.post('/posts/', json=payload,
                                      headers={'Authorization': f'Bearer {test_access_token.get("access_token")}'})
    response_json = response.json()
    yield response
    # Once the tests are done delete the post
    response = await test_client.delete(f'/posts/{response_json.get("id")}', headers={'Authorization': f'Bearer {test_access_token.get("access_token")}'})
