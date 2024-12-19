from django.urls import path
from . import views
from .views import your_shelves, stats, your_reviews, create_profile, profile_view, update_profile

app_name = 'reviews'

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('shelves/', views.your_shelves, name='your_shelves'),  # "Your Shelves" page
    path('book_hub/', views.book_hub, name='book_hub'),  # "Book Hub" page
    path('stats/', stats, name='stats'),  # Stats page
    path('reviews/', your_reviews, name='your_reviews'),  # Your reviews page
    path('review/<int:pk>/', views.review_detail, name='review_detail'), 
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/add-review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('book/<int:book_id>/add-to-shelf/', views.add_to_shelf, name='add_to_shelf'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/', profile_view, name='profile'),
    path("profile/", views.profile_view, name="profile"),
    path('your-shelves/', your_shelves, name='your_shelves'),
    path('update-progress/<int:review_id>/', views.update_progress, name='update_progress'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('add/', views.add_book, name='add_book'),
    
]