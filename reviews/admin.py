from django.contrib import admin
from .models import Book, Review, UserProfile
from .forms import BookForm


admin.site.register(Review)
admin.site.register(UserProfile)

class BookAdmin(admin.ModelAdmin):
    form = BookForm

admin.site.register(Book, BookAdmin)