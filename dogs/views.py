from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .forms import DogProfileSettingsForm
from .models import Dog


class DogAddView(LoginRequiredMixin, CreateView):
    template_name = "dogs/add_dog.html"
    model = Dog
    fields = ["name", "age", "sex", "breed", "size", "bio", "photo"]
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogsListView(LoginRequiredMixin, ListView):
    template_name = "dogs/dogs.html"
    model = Dog
    context_object_name = "dogs"

    def get_queryset(self):
        return Dog.objects.filter(owner=self.request.user)


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = "dogs/profile.html"
    context_object_name = "dog"


class DogProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "dogs/profile_settings.html"
    model = Dog
    form_class = DogProfileSettingsForm
    success_url = reverse_lazy("dogs")
    context_object_name = "dog"

