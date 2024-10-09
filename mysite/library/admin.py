from django.contrib import admin
from .models import Book, BookInstance, Author, Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'display_genre']


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance)
admin.site.register(Author)
admin.site.register(Genre)
