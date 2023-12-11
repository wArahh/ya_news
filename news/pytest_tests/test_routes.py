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
def test_detail(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
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
def test_edit_delete_comments(client, admin_client, comment, root):
    url = reverse(root, args=(comment.pk,))
    login_url = reverse('users:login')
    response = client.get(url)
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND







