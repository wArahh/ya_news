from http import HTTPStatus

import pytest
from django.urls import reverse
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
def test_detail(client, detail_url):
    response = client.get(detail_url)
    assert response.status_code == HTTPStatus.OK


def test_delete_edit(author_client, comment, edit_url, delete_url):
    urls = edit_url, delete_url
    for url in urls:
        response = author_client.get(url)
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_edit_delete_comments(client, admin_client, news, edit_url, delete_url):
    urls = edit_url, delete_url
    for url in urls:
        login_url = reverse('users:login')
        response = client.get(url)
        expected_url = f'{login_url}?next={url}'
        assertRedirects(response, expected_url)
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
