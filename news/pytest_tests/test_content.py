import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_pagination(client, bulk_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_sorting(news, client, bulk_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_sorting(comment_sort, detail_url, news, client):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_post_comment_authorized(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context


@pytest.mark.django_db
def test_post_comment_not_authorized(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context
