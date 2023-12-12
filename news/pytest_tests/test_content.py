import pytest
from django.conf import settings


@pytest.mark.django_db
def test_pagination(client, bulk_news):
    client.get('news:home')
    news_count = len(bulk_news)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_sorting(client, bulk_news):
    client.get('news:home')
    all_dates = [news.date for news in bulk_news]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_sorting(bulk_comments):
    all_dates = [comment.created for comment in bulk_comments]
    sorted_comments = sorted(all_dates, reverse=True)
    assert all_dates == sorted_comments


@pytest.mark.django_db
def test_post_comment_authorized(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context


@pytest.mark.django_db
def test_post_comment_not_authorized(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context
