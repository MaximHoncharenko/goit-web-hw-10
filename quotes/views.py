from django.shortcuts import render

from .migrate import author
from .utils import get_mongodb, get_top_tags
from bson import ObjectId
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, AuthorForm, QuoteForm
from .models import Author
from django.contrib.auth.decorators import login_required
from django.http import Http404

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

    # Додаємо автора до кожної цитати, використовуючи ObjectId
    for quote in quotes_on_page:
        author_id = quote.get('author')  # Отримуємо ObjectId автора з цитати
        if author_id:  # Перевіряємо, чи є author_id
            # Пошук автора за ObjectId
            author = db.authors.find_one({'_id': ObjectId(author_id)})
            if author:
                quote['author'] = author  # Додаємо автора до цитати
                quote['author_id'] = author_id  # Додаємо author_id окремо, щоб використовувати його в шаблоні
            else:
                print(f"Author not found for author_id: {author_id}")
        else:
            quote['author'] = None  # Якщо немає автора, встановлюємо None
            quote['author_id'] = None  # Якщо немає автора, додаємо None для author_id

    return render(request, "quotes/index.html", context={
        "quotes_on_page": quotes_on_page,
        "top_tags": top_tags  # Передаємо top_tags на головну сторінку
    })






def quotes_by_tag(request, tag):
    db = get_mongodb()

    # Шукаємо цитати, що мають цей тег
    quotes = list(db.quotes.find({"tags": tag}))

    # Для кожної цитати перевіряємо наявність автора і додаємо їх інформацію
    for quote in quotes:
        if quote.get('author'):
            author = db.authors.find_one({"_id": quote['author']})  # Шукаємо автора по його _id
            quote['author_name'] = author.get('fullname', 'Unknown Author')  # Додаємо ім'я автора
        else:
            quote['author_name'] = 'Unknown Author'

    # Отримуємо топ-10 тегів
    top_tags = get_top_tags()

    return render(request, "quotes/quotes_by_tag.html", context={
        "quotes": quotes,
        "tag": tag,
        "top_tags": top_tags,
    })

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main')  # Перенаправлення на головну сторінку
    else:
        form = CustomUserCreationForm()

    return render(request, "quotes/register.html", {"form": form})

# Вхід користувача
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')  # Перенаправлення на головну сторінку
    else:
        form = AuthenticationForm()

    return render(request, "quotes/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect('main')  # Перенаправлення на головну сторінку

# Додавання нового автора
@login_required  # Тільки для авторизованих користувачів
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')  # Перенаправлення на головну сторінку
    else:
        form = AuthorForm()

    return render(request, "quotes/add_author.html", {"form": form})

# Додавання нової цитати
@login_required  # Тільки для авторизованих користувачів
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')  # Перенаправлення на головну сторінку
    else:
        form = QuoteForm()

    return render(request, "quotes/add_quote.html", {"form": form})

def author_detail(request, author_id):
    """Відображення сторінки автора"""
    try:
        author = Author.objects.get(id=author_id)  # Використовуємо стандартне ціле число
    except Author.DoesNotExist:
        raise Http404("Author not found")

    return render(request, "quotes/author_detail.html", {"author": author})
