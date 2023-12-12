from http import HTTPStatus
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'root',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_main(client, root):
    url = reverse(root)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail(client, news, detail_url):
    response = client.get(detail_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'root',
    ('news:edit', 'news:delete'),
)
def test_delete_edit(author_client, comment, root):
    url = reverse(root, args=(comment.pk,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'root',
    ('news:edit', 'news:delete'),
)
def test_edit_delete_comments(client, admin_client, news, redirect_login_url, root):
    url = reverse(root, args=(news.pk,))
    login_url = reverse('users:login')
    response = client.get(url)
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND







