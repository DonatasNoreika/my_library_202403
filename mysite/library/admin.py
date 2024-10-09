from django.contrib import admin
from .models import Book, BookInstance, Author, Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'display_genre']

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'due_back', 'status']
    list_filter = ['book', 'status', 'due_back']

    fieldsets = (
        ("Pagrindinis", {"fields": ("uuid", "book")}),
        ("Pasiekiamumas", {"fields": ("due_back", "status")}),
    )

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Author)
admin.site.register(Genre)
