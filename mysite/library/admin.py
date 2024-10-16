from django.contrib import admin
from .models import Book, BookInstance, Author, Genre

class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", 'last_name', 'display_books']

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra =  0
    can_delete = False
    readonly_fields = ['uuid']
    fields = ['uuid', 'due_back', 'status']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'display_genre']
    inlines = [BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'due_back', "reader", 'status', 'is_overdue']
    list_filter = ['book', 'status', 'due_back']
    search_fields = ['uuid', 'book__title', 'book__author__first_name', 'book__author__last_name']
    list_editable = ['due_back', "reader", 'status']

    fieldsets = (
        ("Pagrindinis", {"fields": ("uuid", "book")}),
        ("Pasiekiamumas", {"fields": ("due_back", "status", "reader")}),
    )

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
