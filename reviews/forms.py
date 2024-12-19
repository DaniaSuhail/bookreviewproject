from django import forms
from .models import BookReview
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from reviews.models import UserProfile

# Define genre choices
GENRE_CHOICES = [
    ("Fantasy", "Fantasy"),
    ("Magic", "Magic"),
    ("Historical", "Historical"),
    ("Science Fiction", "Science Fiction"),
    ("Mystery", "Mystery"),
    ("Adventure", "Adventure"),
    ("Romance", "Romance"),
    ("Thriller", "Thriller"),
    ("Suspense", "Suspense"),
    ("Biography", "Biography"),
    ("Contemporary Fiction", "Contemporary Fiction"),
    ("Crime", "Crime"),
    ("Classics", "Classics"),
    ("Non Fiction", "Non Fiction"),
    ("Children", "Children"),
    ("Young Adult", "Young Adult"),
    ("Literature", "Literature"),
    ("Distopian", "Distopian"),
]


class BookForm(forms.ModelForm):
    genre = forms.MultipleChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Select Genres"
    )

    class Meta:
        model = Book
        fields = ["title", "author", "genre", "description", "image"]

    def clean_genre(self):
        # Ensure the genres are saved as a list for the JSONField
        genre = self.cleaned_data["genre"]
        return genre


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search Books')

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email Address'
    }))
    bio = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Short Bio'
    }))
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class ReadingGoalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['reading_goal']

from django import forms
from reviews.models import UserProfile
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'reading_goal']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something about yourself...'}),
            'reading_goal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Set your reading goal'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'reading_goal', 'profile_picture']

class AddBookForm(forms.ModelForm):
    genre = forms.MultipleChoiceField(
        choices=GENRE_CHOICES,  # Use predefined choices
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),  # Render as checkboxes
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }