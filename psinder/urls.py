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
from user_messages import views as messages

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home page
    path('', dating.MainPageView.as_view(), name="home-page"),
    path('about/', dating.AboutAppView.as_view(), name="about-app"),
    # Users
    path('register/', dating.UserCreateView.as_view(), name="register"),
    path('login/', dating.UserLoginView.as_view(), name="login"),
    path('logout/', dating.UserLogoutView.as_view(), name="logout"),
    path('dashboard/', dating.UserDashboardView.as_view(), name="dashboard"),
    path('profile/<str:slug>/', dating.UserProfileView.as_view(), name="user-profile"),
    path('profiles_search/', dating.SearchProfilesView.as_view(), name="search-profiles"),
    path('settings/<int:pk>/', dating.UserSettingsView.as_view(), name="settings"),
    path('settings/<int:pk>/change_password/', dating.UserChangePasswordView.as_view(), name="change-password"),
    path('settings/<int:pk>/change_address/', dating.UserChangeAddressView.as_view(), name="change-address"),
    # Messages
    path('inbox/', messages.ThreadsList.as_view(), name="inbox"),
    path('inbox/create_thread/', messages.ThreadCreate.as_view(), name="create-thread"),
    path('inbox/<int:pk>/', messages.ThreadView.as_view(), name="thread"),
    path('inbox/<int:pk>/create_message/', messages.MessageCreate.as_view(), name="create-message"),
    # Meetings
    path('meetings/', dating.MeetingListView.as_view(), name="meetings"),
    path('add_meeting/', dating.MeetingAddView.as_view(), name="add-meeting"),
    path('meeting/<int:pk>/', dating.MeetingDetailsView.as_view(), name="meeting"),
    path('meeting/<int:pk>/edit/', dating.MeetingUpdateView.as_view(), name="edit-meeting"),
    path('meeting/<int:pk>/delete/', dating.MeetingDeleteView.as_view(), name="delete-meeting"),
    path('meeting/<int:pk>/join/', dating.MeetingJoinView.as_view(), name="join-meeting"),
    path('meetings/search/', dating.MeetingSearchView.as_view(), name="search-meetings"),
    # Dogs
    path('add_dog/', dogs.DogAddView.as_view(), name="add-dog"),
    path('dogs/', dogs.DogsListView.as_view(), name="dogs"),
    path('dog_profile/<int:pk>/', dogs.DogDetailView.as_view(), name="dog-profile"),
    path('dog_profile/<int:pk>/edit/', dogs.DogProfileUpdateView.as_view(), name="edit-dog-profile"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
