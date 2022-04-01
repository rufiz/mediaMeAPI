import httpx
import pytest

from fastapi import status

from app.schemas import PostDB


@pytest.mark.asyncio
class TestPosts:
    async def test_get_posts_valid(self, test_client: httpx.AsyncClient):
        # Extract all the posts
        response = await test_client.get('/posts/')
        # Assert it returns 200 status code
        assert response.status_code == status.HTTP_200_OK

    async def test_get_post_valid(self):
        # Create a post
        # Return the created post
        # Delete the created post
        pass

    async def test_create_post_valid(self):
        # Create a post
        # Read the response content
        # Assert the status code 201 and content of
        # the response post is the same as the created one
        pass

    async def test_update_post_valid(self):
        # Create a post
        # Update it
        # Assert the response from the updated post is the same as
        # the response post
        pass

    async def test_delete_post_valid(self):
        # Create a post
        # Delete the post
        # Assert the response code is 204
        pass


@pytest.fixture
async def test_create_post(test_client: httpx.AsyncClient, test_access_token):
    # Create the payload with PostDB schema
    payload = PostDB(title='Pytest Fixture',
                     content='Created with Pytest').dict()
    # Post it to the /posts/ endpoint
    response = await test_client.post('/posts/', json=payload,
                                      headers={'Authorization': f'Bearer {test_access_token.get("access_token")}'})
    yield response
    # Once the tests are done delete the post
    await test_client.delete(f'/posts/{response.get("id")}', headers={'Authorization': f'Bearer {test_access_token.get("access_token")}'})
