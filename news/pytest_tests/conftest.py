from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def antiowner(django_user_model):
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Название',
        text='Текст',
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст',
    )


@pytest.fixture
def bulk_news(author):
    return News.objects.bulk_create(
        News(title=f'Новость {index}', text='Текст',
             date=datetime.now() - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_sort(author, news, comment):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'Текст'
    }


@pytest.fixture
def url_to_comments(news):
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = news_url + '#comments'
    return url_to_comments


@pytest.fixture
def edited_form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'Редактированный текст'
    }


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', kwargs={'pk': news.pk})


@pytest.fixture
def edit_url(news):
    return reverse('news:edit', kwargs={'pk': news.pk})


@pytest.fixture
def delete_url(news):
    return reverse('news:delete', kwargs={'pk': news.pk})


@pytest.fixture
def redirect_login_url(news, detail_url):
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={detail_url}'
    return expected_url
