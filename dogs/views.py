from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

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



