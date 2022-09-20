from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from .forms import UserCreateForm, UserLoginForm, UserProfileSettingsForm, UserChangePasswordForm, UserAddressForm
from dogs.models import Dog

User = get_user_model()


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        user_profiles_count = User.objects.all().count()
        dog_profiles_count = Dog.objects.all().count()
        context = {
            "user_profiles_count": user_profiles_count,
            "dog_profiles_count": dog_profiles_count,
        }
        return render(request, "base.html", context=context)


class AboutAppView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dating/about.html")


class UserCreateView(FormView):
    form_class = UserCreateForm
    template_name = "dating/register.html"
    success_url = reverse_lazy("home-page")

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd.get("username")
        password = cd.get("password1")
        email = cd.get("email")
        first_name = cd.get("first_name")
        last_name = cd.get("last_name")
        gender = cd.get("gender")
        dob = cd.get("dob")
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob
        )
        return super().form_valid(form)


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "dating/login.html"
    success_url = reverse_lazy("home-page")

    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd.get("username")
        password = cd.get("password")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("home-page")


class UserDashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "dating/dashboard.html")


class UserSettingsView(LoginRequiredMixin, UpdateView):
    template_name = "dating/profile_settings.html"
    model = User
    form_class = UserProfileSettingsForm
    success_url = reverse_lazy("dashboard")


class UserChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserChangePasswordForm()
        return render(request, "dating/change_password.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            user_pk = kwargs.get("pk")
            user = User.objects.get(pk=user_pk)
            new_password = form.cleaned_data["new_password"]
            user.set_password(new_password)
            user.save()
            return redirect("settings", user.pk)
        return render(request, "dating/change_password.html", context={"form": form})


class UserChangeAddressView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_pk = kwargs.get("pk")
        user = User.objects.get(pk=user_pk)
        form = UserAddressForm(instance=user.address)
        return render(request, "dating/change_address.html", context={"form": form})
