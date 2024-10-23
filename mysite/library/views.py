from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormMixin
from .models import Book, BookInstance, Author, BookReview
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import BookReviewForm, UserUpdateForm, ProfileUpdateForm, BookInstanceUpdateForm
from django.utils.translation import gettext as _

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


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse("book", kwargs={"pk": self.object.pk})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

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
                # messages.error(request, f"Vartotojas vardas {username} užimtas!")
                messages.error(request, _('Username %s already exists!') % username)
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Email %s already exists!') % email)
                    return redirect("register")
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as err:
                        for error in err:
                            messages.error(request, error)
                        return redirect("register")
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, _('User %s registered!') % username)
                    return redirect("login")

        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect("register")
    return render(request, template_name="registration/register.html")


@login_required
def profile(request):
    if request.method == "POST":
        new_email = request.POST['email']
        new_first_name = request.POST['first_name']
        new_last_name = request.POST['last_name']
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f"Vartotojas su el. paštu {new_email} jau užregistruotas!")
            return redirect("profile")
        if user_update_form.is_valid() and profile_update_form.is_valid():
            request.user.first_name = new_first_name
            request.user.last_name = new_last_name
            user_update_form.save()
            profile_update_form.save()
            messages.info(request, "Profilis atnaujintas")
            return redirect("profile")

    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, template_name="profile.html", context=context)

class BookInstanceListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = BookInstance
    context_object_name = "copies"
    template_name = "copies.html"

    def test_func(self):
        return self.request.user.profile.is_employee


class BookInstanceDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = BookInstance
    context_object_name = "copy"
    template_name = "copy.html"

    def test_func(self):
        return self.request.user.profile.is_employee


class BookInstanceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = BookInstance
    template_name = "copy_form.html"
    fields = ['book', 'status']
    success_url = "/library/copies/"

    def test_func(self):
        return self.request.user.profile.is_employee


class BookInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    template_name = "copy_form.html"
    success_url = "/library/copies/"
    # fields = ['book', 'status', 'reader', 'due_back']
    form_class = BookInstanceUpdateForm

    def test_func(self):
        return self.request.user.profile.is_employee


class BookInstanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookInstance
    template_name = "copy_delete.html"
    context_object_name = 'copy'
    success_url = "/library/copies/"

    def test_func(self):
        return self.request.user.profile.is_employee


class BookReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookReview
    template_name = "review_update.html"
    fields = ['content']
    # success_url = "/library/books/"

    def get_success_url(self):
        return reverse("book", kwargs={"pk": self.object.book.pk})

    def test_func(self):
        return self.get_object().reviewer == self.request.user


class BookReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BookReview
    template_name = "review_delete.html"
    context_object_name = "review"
    # success_url = "/library/books/"

    def get_success_url(self):
        return reverse("book", kwargs={"pk": self.object.book.pk})

    def test_func(self):
        return self.get_object().reviewer == self.request.user