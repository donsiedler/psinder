from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import UserCreateForm, UserLoginForm

User = get_user_model()


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "base.html")


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
