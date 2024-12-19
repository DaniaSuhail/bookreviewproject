from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view

app_name = 'accounts'


from django.urls import path
from .views import register_view, create_profile_view

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('create-profile/', create_profile_view, name='create_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]