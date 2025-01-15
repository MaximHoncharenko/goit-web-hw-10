from django.shortcuts import render
from .utils import get_mongodb
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    db = get_mongodb()
    quotes = list(db.quotes.find())  # Отримуємо всі цитати
    per_page = 10  # Кількість цитат на сторінку

    paginator = Paginator(quotes, per_page)
    page = request.GET.get('page', 1)  # Номер сторінки
    try:
        quotes_on_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        quotes_on_page = paginator.page(1)

    return render(request, "quotes/index.html", context={"quotes_on_page": quotes_on_page})


def quotes_by_tag(request, tag):
    db = get_mongodb()
    quotes = list(db.quotes.find({"tags": tag}))  # Знайти цитати з конкретним тегом
    return render(request, "quotes/quotes_by_tag.html", context={"quotes": quotes, "tag": tag})