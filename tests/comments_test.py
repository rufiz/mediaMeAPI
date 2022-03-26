import httpx
import pytest

from fastapi import status

from app.schemas import CommentDB


@pytest.mark.asyncio
class TestComments:
    async def test_create_comment_valid(self, test_create_comment):
        # Create a comment
        response = test_create_comment
        response_json = response.json()

        assert response_json.get('content') == 'Test Content'
        assert response_json.get('post_id') == 9
        assert response.status_code == status.HTTP_201_CREATED

    async def test_delete_comment_valid(self, test_create_comment, test_client: httpx.AsyncClient, test_access_token):
        # Create a comment first
        response_comment = test_create_comment
        response_comment_json = response_comment.json()
        # Delete the created comment
        response_from_delete = await test_client.delete(f'/comments/{response_comment_json.get("id")}',
                                                        headers={'Authorization': f'Bearer {test_access_token.get("access_token")}',
                                                                 'typ': 'JWT'})
        # Try to retrive the deleted comment
        response_from_get_deleted_comment = await test_client.get(f'/comments/{response_comment_json.get("id")}')

        assert response_from_delete.status_code == status.HTTP_204_NO_CONTENT
        assert response_from_get_deleted_comment.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_comment_valid(self, test_create_comment, test_client: httpx.AsyncClient, test_access_token):
        # Create a comment first
        response_comment = test_create_comment
        response_comment_json = response_comment.json()
        # Get the comment by id
        extracted_comment = await test_client.get(f'/comments/{response_comment_json.get("id")}',
                                                  headers={'Authorization': f'Bearer {test_access_token.get("access_token")}'})

        assert extracted_comment.status_code == status.HTTP_200_OK
        assert response_comment_json.get('content') == 'Test Content'
        assert response_comment_json.get('post_id') == 9


@pytest.fixture
async def test_create_comment(test_client: httpx.AsyncClient, test_access_token):
    # Create a comment
    payload = CommentDB(content='Test Content', post_id=9).dict()

    response = await test_client.post('/comments/', json=payload,
                                      headers={'Authorization': f'Bearer {test_access_token.get("access_token")}',
                                               'typ': 'JWT'})
    response_json = response.json()
    yield response
    # Delete the created comment
    response = await test_client.delete(f'/comments/{response_json.get("id")}', headers={'Authorization': f'Bearer {test_access_token.get("access_token")}',
                                                                                         'typ': 'JWT'})
