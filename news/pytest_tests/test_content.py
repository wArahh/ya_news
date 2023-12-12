from http import HTTPStatus
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects
from django.conf import settings


@pytest.mark.django_db
def test_pagination(client, bulk_news):
    client.get('news:home')
    news_count = len(bulk_news)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_sorting(client, news, bulk_news):
    client.get('news:home')
    all_dates = [news.date for news in bulk_news]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_sorting(client, comment, news, bulk_comments):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    client.get(url)
    all_dates = [comment.created for comment in bulk_comments]
    sorted_comments = sorted(all_dates, reverse=True)
    assert all_dates == sorted_comments


@pytest.mark.django_db
def test_post_comment_authorized(author_client, comment, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = author_client.get(url)
    assert 'form' in response.context


@pytest.mark.django_db
def test_post_comment_not_authorized(client, comment, news):
    url = reverse('news:detail', kwargs={'pk': news.pk})
    response = client.get(url)
    assert 'form' not in response.context





