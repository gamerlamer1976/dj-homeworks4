from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'

    # Получаем статьи, сортируем по дате и оптимизируем запросы к БД.
    # prefetch_related('scopes__tag') достает и промежуточную таблицу, и сами названия тегов.
    articles = Article.objects.order_by('-published_at').prefetch_related('scopes__tag')

    # Ключ 'object_list' используется, так как именно его ожидает цикл {% for article in object_list %} в шаблоне
    context = {
        'object_list': articles
    }

    return render(request, template, context)
