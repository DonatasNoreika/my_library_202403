from django.db import models
import uuid

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(verbose_name="Vardas", max_length=100)
    last_name = models.CharField(verbose_name="Pavardė", max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200, help_text='Įveskite knygos žanrą (pvz. detektyvas)')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=200)
    summary = models.TextField(verbose_name="Aprašymas", max_length=2000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField(verbose_name="ISBN", max_length=13, help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
    genre = models.ManyToManyField(to="Genre", verbose_name="Žanrai", help_text='Išrinkite žanrą (-us) šiai knygai')

    def __str__(self):
        return f"{self.title} ({self.author})"

class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey(to="Book", verbose_name="Knyga", on_delete=models.CASCADE, related_name="instances")
    due_back = models.DateField(verbose_name="Bus prieinama", null=True, blank=True)
    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )
    status = models.CharField(verbose_name="Būsena", max_length=1, choices=LOAN_STATUS, default="a", blank=True)

    def __str__(self):
        return f"{self.uuid} - {self.book.title} ({self.get_status_display()}, {self.due_back})"