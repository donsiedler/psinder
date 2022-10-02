from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .forms import DogProfileSettingsForm, DogCreateForm
from .models import Dog


class DogAddView(LoginRequiredMixin, CreateView):
    template_name = "dogs/add_dog.html"
    model = Dog
    form_class = DogCreateForm
    success_url = reverse_lazy("dogs")

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


class DogProfileUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # Prevents the user from editing other users dog profiles
        dog_owner = Dog.objects.get(pk=self.kwargs["pk"]).owner
        return self.request.user.is_authenticated and self.request.user == dog_owner

    template_name = "dogs/profile_settings.html"
    model = Dog
    form_class = DogProfileSettingsForm
    success_url = reverse_lazy("dogs")
    context_object_name = "dog"

