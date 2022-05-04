from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    #path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', LoginView.as_view(template_name='firesale/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/firesale/login'), name="logout")
]
