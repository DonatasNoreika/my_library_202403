from django.contrib.auth import password_validation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        'num_visits': num_visits,
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


class UserBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "user_copies.html"
    context_object_name = "copies"
    # login_url = '/library/accounts/login/'

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojas vardas {username} užimtas!")
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Vartotojas su el. paštu {email} jau užregistruotas!")
                    return redirect("register")
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as err:
                        for error in err:
                            messages.error(request, error)
                        return redirect("register")
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f"Vartotojas {username} užregistruotas!")
                    return redirect("login")

        else:
            messages.error(request, "Slaptažodžiai nesutampa!")
            return redirect("register")
    return render(request, template_name="registration/register.html")

