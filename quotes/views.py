from django.shortcuts import render
from .utils import get_mongodb, get_top_tags
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

    top_tags = get_top_tags()  # Отримуємо топ-10 тегів

    return render(request, "quotes/index.html", context={
        "quotes_on_page": quotes_on_page,
        "top_tags": top_tags  # Передаємо top_tags на головну сторінку
    })

def quotes_by_tag(request, tag):
    db = get_mongodb()
    
    # Шукаємо цитати, що мають цей тег
    quotes = list(db.quotes.find({"tags": tag}))
    
    # Отримуємо топ-10 тегів
    top_tags = get_top_tags()
    
    return render(request, "quotes/quotes_by_tag.html", context={
        "quotes": quotes,
        "tag": tag,
        "top_tags": top_tags  # Передаємо top_tags
    })