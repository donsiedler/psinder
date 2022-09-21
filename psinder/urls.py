"""psinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from dating import views as dating
from dogs import views as dogs

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dating
    path('', dating.MainPageView.as_view(), name="home-page"),
    path('about/', dating.AboutAppView.as_view(), name="about-app"),
    path('register/', dating.UserCreateView.as_view(), name="register"),
    path('login/', dating.UserLoginView.as_view(), name="login"),
    path('logout/', dating.UserLogoutView.as_view(), name="logout"),
    path('dashboard/', dating.UserDashboardView.as_view(), name="dashboard"),
    path('settings/<int:pk>/', dating.UserSettingsView.as_view(), name="settings"),
    path('settings/<int:pk>/change_password/', dating.UserChangePasswordView.as_view(), name="change-password"),
    path('settings/<int:pk>/change_address/', dating.UserChangeAddressView.as_view(), name="change-address"),
    # Dogs
    path('add_dog/', dogs.DogAddView.as_view(), name="add-dog"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
