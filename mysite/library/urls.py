from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("authors/", views.authors, name="authors"),
    path("authors/<int:author_id>", views.author, name='author'),
    path("books/", views.BookListView.as_view(), name="books"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name="book"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("usercopies/", views.UserBookInstanceListView.as_view(), name="user_copies"),
    path("copies/", views.BookInstanceListView.as_view(), name="copies"),
    path("copies/<int:pk>", views.BookInstanceDetailView.as_view(), name="copy"),
    path("copies/new", views.BookInstanceCreateView.as_view(), name="copies_new"),
    path("copies/<int:pk>/update", views.BookInstanceUpdateView.as_view(), name="copies_update"),
    path("copies/<int:pk>/delete", views.BookInstanceDeleteView.as_view(), name="copies_delete"),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]