from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import generic

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
    context = {
        "authors": authors,
    }
    return render(request, template_name="authors.html", context=context)


def author(request, author_id):
    return render(request, template_name="author.html", context={"author": Author.objects.get(pk=author_id)})

class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
