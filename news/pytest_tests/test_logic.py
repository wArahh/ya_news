from http import HTTPStatus

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_post_comment(client, detail_url, redirect_login_url,
                      admin_client, form_data, url_to_comments):
    response = client.post(detail_url, form_data)
    assertRedirects(response, redirect_login_url)
    response = admin_client.post(detail_url, form_data)
    assertRedirects(response, url_to_comments)


@pytest.mark.django_db
def test_bad_comment(author_client, detail_url):
    bad_word = {'text': BAD_WORDS[0]}
    response = author_client.post(detail_url, data=bad_word)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_edit_and_comment(url_to_comments,
                          author_client, edited_form_data,
                          comment, edit_url, delete_url):
    response = author_client.post(edit_url, data=edited_form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == 'Редактированный текст'
    author_client.delete(delete_url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_edit_and_comment_anonymous(form_data, client, comment,
                                    edit_url, delete_url):
    response = client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст'
    client.delete(delete_url)
    assert Comment.objects.count() == 1
