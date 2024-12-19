from django.shortcuts import render, get_object_or_404
from .models import Book, Review, Shelf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import BookReview
from .models import UserProfile
from .forms import BookForm  # We'll create this form next
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from django.urls import reverse
from django.db.models import Avg
from django.shortcuts import redirect
from django.http import JsonResponse  
from django.db.models import Q
from django.contrib import messages
from .forms import UpdateProfileForm
from reviews.models import Review
from collections import Counter
from django.db.models import Count
from .models import Review 
from reviews.forms import UserProfileForm

def home(request):
    # Get the first 4 books to display as featured
    featured_books = Book.objects.all()[:6]
    # Use timestamp instead of created_at for sorting
    recent_reviews = Review.objects.select_related('book').order_by('-timestamp')[:5]
    context = {
        'featured_books': featured_books,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'reviews/home.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def all_reviews(request):
    reviews = BookReview.objects.all()
    return render(request, 'reviews/all_reviews.html', {'reviews': reviews})

# View to add a new book review
@login_required
def add_review(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        # Create or update the review
        Review.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={'content': content, 'rating': rating},
        )

        print(f"Review submitted for {book.title}: {content} (Rating: {rating})")  # Debugging
        return redirect("reviews:book_detail", pk=book_id)

    return redirect("reviews:book_detail", pk=book_id)

def book_search(request):
    form = SearchForm()
    books = None

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Search books by title or author (or other fields as needed)
            books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    
    return render(request, 'reviews/book_search.html', {'form': form, 'books': books})

def book_search(request):
    query = request.GET.get('query', '')
    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request, 'reviews/book_list.html', {'books': books, 'query': query})

def book_hub(request):
    # Main Book Hub page with navigation
    return render(request, 'reviews/book_hub.html')


from django.shortcuts import render
from .models import Shelf

def your_shelves(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # Fetch books for each shelf category
    currently_reading = Shelf.objects.filter(user=request.user, shelf='Currently Reading')
    want_to_read = Shelf.objects.filter(user=request.user, shelf='Want to Read')
    finished_reading = Shelf.objects.filter(user=request.user, shelf='Finished')

    # Debugging: Print the filtered books
    print("Currently Reading:", list(currently_reading))
    print("Want to Read:", list(want_to_read))
    print("Finished Reading:", list(finished_reading))

    context = {
        'currently_reading': currently_reading,
        'want_to_read': want_to_read,
        'finished_reading': finished_reading,
    }

    return render(request, 'reviews/your_shelves.html', context)

from collections import Counter
from django.shortcuts import render
from django.db.models import Count

def stats(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # Fetch finished books from Shelf
    finished_reviews = Shelf.objects.filter(user=request.user, shelf="Finished")

    # Flatten all genres into a single list
    all_genre = []
    for entry in finished_reviews:
        # Assuming `entry.book.genre` is a list
        all_genre.extend(entry.book.genre)  # No need to split if it's already a list

    # Count genre
    genre_counts = Counter(all_genre)
    genre_data = [{'genre': genre, 'count': count} for genre, count in genre_counts.items()]

    # Reading goal progress
    reading_goal = request.user.userprofile.reading_goal or 0
    total_finished = finished_reviews.count()
    progress_percentage = (total_finished / reading_goal * 100) if reading_goal > 0 else 0

    # Most Read Authors
    author_counts = (
        finished_reviews.values('book__author')
        .annotate(count=Count('book__author'))
        .order_by('-count')
    )
    authors_data = [{'author': item['book__author'], 'count': item['count']} for item in author_counts]

    context = {
        'genre_data': genre_data,
        'reading_goal': reading_goal,
        'progress_percentage': progress_percentage,
        'authors_data': authors_data,
    }
    return render(request, 'reviews/stats.html', context)


def review_detail(request, pk):
    # Fetch the specific review using the primary key (pk)
    review = get_object_or_404(Review, pk=pk)
    context = {
        'review': review,
    }
    return render(request, 'review_detail.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book, 
    }
    return render(request, 'book_detail.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = Review.objects.filter(book=book)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Handle form submission for adding a review
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if content and rating:
            Review.objects.create(
                book=book,
                user=request.user.username,
                content=content,
                rating=int(rating)
            )
            return HttpResponseRedirect(reverse('reviews:book_detail', args=[pk]))

    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),
    }
    return render(request, 'reviews/book_detail.html', context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        if content and rating:
            review.content = content
            review.rating = int(rating)
            review.save()
            return redirect('reviews:book_detail', pk=review.book.id)
    context = {'review': review}
    return render(request, 'reviews/edit_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        book_id = review.book.id
        review.delete()
        return redirect('reviews:book_detail', pk=book_id)
    context = {'review': review}
    return render(request, 'reviews/delete_review.html', context)

from django.db.models import Q

def explore(request):
    search_query = request.GET.get('search', '').strip()  # Get and clean the search query
    genre_filter = request.GET.get('genre', '').strip()  # Get and clean the genre filter

    books = Book.objects.all()

    # Filter by title or author
    if search_query:
        books = books.filter(
            title__icontains=search_query  # Case-insensitive search for title
        ) | books.filter(
            author__icontains=search_query  # Case-insensitive search for author
        )

    # Filter by genre
    if genre_filter:
        books = books.filter(genre__icontains=genre_filter)

    context = {'books': books}
    return render(request, 'reviews/explore.html', context)



# views.py
def book_hub(request):
    total_books_read = 10  # Example value, replace with your calculation logic
    reading_goal = 20  # Example value, replace with your logic
    
    if reading_goal > 0:
        progress_percentage = (total_books_read / reading_goal) * 100
    else:
        progress_percentage = 0  # Avoid division by zero
    
    context = {
        "total_books_read": total_books_read,
        "reading_goal": reading_goal,
        "progress_percentage": progress_percentage,
        # Other context data
    }
    return render(request, "reviews/book_hub.html", context)

def your_reviews(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    reviews = Review.objects.filter(user=request.user)

    context = {
        'reviews': reviews,
    }
    return render(request, 'reviews/your_reviews.html', context)

def update_reading_goal(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ReadingGoalForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('reviews:stats')
    else:
        form = ReadingGoalForm(instance=user_profile)

    return render(request, 'reviews/update_goal.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from .models import Shelf, Book

from django.shortcuts import get_object_or_404, redirect
from .models import Shelf, Book

def add_to_shelf(request, book_id):
    if request.method == "POST":
        # Get the selected shelf value from the form
        shelf = request.POST.get("shelf")
        print(f"Shelf selected: {shelf}")  # Debugging

        # Get the book instance
        book = get_object_or_404(Book, id=book_id)

        # Check if the book is already associated with the user in any shelf
        Shelf.objects.filter(user=request.user, book=book).delete()  # Remove from other shelves

        # Add the book to the selected shelf
        Shelf.objects.create(user=request.user, book=book, shelf=shelf)

        print(f"Moved {book.title} to the {shelf} shelf.")  # Debugging

        return redirect("reviews:your_shelves")

    return redirect("reviews:your_shelves")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def update_profile(request):
    # Fetch or create the UserProfile instance for the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(user_id=request.user.id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('reviews:profile')  # Redirect to profile page after successful update
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'reviews/profile_update.html', {'form': form})

def update_progress(request, review_id):
    if request.method == "POST":
        progress = request.POST.get("progress")
        review = get_object_or_404(Review, id=review_id, user=request.user)
        
        # Update progress and save
        review.progress = min(max(int(progress), 0), 100)  # Ensure progress is between 0 and 100
        review.save()

        # Redirect back to the "Your Shelves" page
        return redirect("reviews:your_shelves")  # Replace with the actual name of your shelves page
    
def stats_view(request):
    reading_goal = request.user.profile.reading_goal if hasattr(request.user, 'profile') else 21

    # Filter books with "Finished" status
    books_finished = Review.objects.filter(user=request.user, status="Finished").count()

    # Calculate progress percentage
    progress_percentage = (books_finished / reading_goal) * 100 if reading_goal > 0 else 0

    # Fetch finished books and calculate genre distribution
    finished_books = Review.objects.filter(user=request.user, status="Finished")
    genre = [book.book.genre for book in finished_books]  # Ensure `book` has a `genre` field
    genre_counts = dict(Counter(genre))

    total_books = sum(genre_counts.values())
    genre_data = {genre: (count / total_books) * 100 for genre, count in genre_counts.items()}

    context = {
        "reading_goal": reading_goal,
        "books_finished": books_finished,
        "progress_percentage": round(progress_percentage, 1),
        "genre_data": genre_data,
    }
    return render(request, "stats.html", context)


from django.contrib.auth.decorators import login_required
from reviews.models import Shelf

@login_required
def profile_view(request):
    try:
        # Check if the user already has a profile
        user_profile = UserProfile.objects.get(user_id=request.user.id)

        # Get the count of books marked as "Finished" in the user's Shelf
        books_read_count = Shelf.objects.filter(user=request.user, shelf="Finished").count()
        review_count = Review.objects.filter(user=request.user).count()

        # Pass the count to the template
        return render(
            request,
            'reviews/profile.html',
            {
                'profile': user_profile,
                'books_read_count': books_read_count,
                'review_count': review_count,
            }
        )
    except UserProfile.DoesNotExist:
        # If no profile exists, redirect to the create profile view
        return redirect('create_profile')


from django.db.utils import IntegrityError
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from reviews.forms import UserProfileForm
from reviews.models import UserProfile

@login_required
def create_profile(request):
    try:
        # If the user already has a profile, redirect to the dashboard
        UserProfile.objects.get(user_id=request.user.id)
        return redirect('reviews:profile')
    except UserProfile.DoesNotExist:
        # Proceed to create a profile
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                user_profile = form.save(commit=False)
                user_profile.user_id = request.user.id  # Associate with the current user
                user_profile.save()
                return redirect('profile_dashboard')
        else:
            form = UserProfileForm()

        return render(request, 'create_profile.html', {'form': form})
    
from .forms import AddBookForm

def add_book(request):
    if request.method == "POST":
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.genre = form.cleaned_data['genre']  # Save genres as a list
            book.save()
            return redirect('reviews:explore')  # Redirect to explore page
    else:
        form = AddBookForm()
    return render(request, 'reviews/add_book.html', {'form': form})
