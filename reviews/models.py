from django.db import models
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from django.contrib.auth.models import User


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
    ("Dystopian", "Dystopian"),
]

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.JSONField(default=list)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)  # ImageField to store images
    
    def __str__(self):
        return self.title
    

class Shelf(models.Model):
    SHELF_CHOICES = [
        ('Currently Reading', 'Currently Reading'),
        ('Want to Read', 'Want to Read'),
        ('Finished', 'Finished'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    shelf = models.CharField(max_length=20, choices=SHELF_CHOICES)

    def __str__(self):
        return f"{self.book.title} - {self.shelf}"

class Review(models.Model):
    STATUS_CHOICES = [
        ('Currently Reading', 'Currently Reading'),
        ('Finished', 'Finished'),
        ('Want to Read', 'Want to Read'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0) 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Want to Read',  # Default value
    )

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"

class UserProfile(models.Model):
    #user_id = models.IntegerField(unique=True)  # Ensure user_id is unique
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='userprofile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    reading_goal = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


def home(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 4)  # Show 4 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'home.html', context)


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Ensure it only runs when a User is created
        UserProfile.objects.create(user=instance)
        print(f"UserProfile created for user: {instance.username}")

