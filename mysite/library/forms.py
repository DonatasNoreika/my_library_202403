from .models import BookReview, Profile, BookInstance
from django import forms
from django.contrib.auth.models import User


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class MyDateInput(forms.DateInput):
    input_type = "date"


class BookInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'status', 'reader', 'due_back']
        widgets = {"due_back": MyDateInput()}