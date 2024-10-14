from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
    }
    return render(request, template_name="index.html", context=context)


def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, per_page=4)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        "authors": paged_authors,
    }
    return render(request, template_name="authors.html", context=context)


def author(request, author_id):
    return render(request, template_name="author.html", context={"author": Author.objects.get(pk=author_id)})

class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 6


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"

def search(request):
    query = request.GET.get("query")
    book_search_results = Book.objects.filter(Q(title__icontains=query) | Q(summary__icontains=query) |
                                              Q(isbn__icontains=query) | Q(author__first_name__icontains=query) |
                                              Q(author__last_name__icontains=query))

    author_search_results = Author.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(description__icontains=query))

    context = {
        "query": query,
        "books": book_search_results,
        "authors": author_search_results,
    }
    return render(request, template_name="search.html", context=context)
