"""fire_sale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from firesale import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firesale/', include('firesale.urls')),
    path('', lambda req: redirect('firesale/', permanent=True)),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', LoginView.as_view(template_name='firesale/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login'), name="logout"),
    path('inbox/', views.inbox, name="inbox"),
    path('my-items/', views.my_items, name="my-items"),
    path('edit-profile/<int:id>', views.edit_profile, name="edit-profile"),
    path('item/<item_id>/', views.item, name='item'),
    path('checkout/<item_id>/', views.checkout, name='checkout'),
    path('payment-information/<item_id>/', views.payment_information, name='payment-information'),
    path('review/<item_id>/', views.review, name='review')
]
