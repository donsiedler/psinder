from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView, ListView, DetailView, DeleteView

from .forms import UserCreateForm, UserLoginForm, UserProfileSettingsForm, UserChangePasswordForm, UserAddressForm, \
    MeetingAddForm, MeetingSearchForm, MeetingJoinForm, SearchProfilesForm
from .models import Address, Meeting
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
        return render(request, "dating/home_page.html", context=context)


class AboutAppView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dating/about.html")


class UserCreateView(FormView):
    form_class = UserCreateForm
    template_name = "dating/register.html"
    success_url = reverse_lazy("dashboard")

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
        user = authenticate(username=username, password=password)
        login(self.request, user)
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


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        user_profile = User.objects.get(slug=slug)
        return render(request, "dating/user_profile.html", context={"user_profile": user_profile})


class UserSettingsView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # Prevents the user from viewing and editing other profiles
        return self.request.user.is_authenticated and self.request.user.pk == self.kwargs["pk"]

    template_name = "dating/profile_settings.html"
    model = User
    form_class = UserProfileSettingsForm
    success_url = reverse_lazy("dashboard")


class UserChangePasswordView(UserPassesTestMixin, View):
    def test_func(self):
        # Prevents the user from changing other users passwords
        return self.request.user.is_authenticated and self.request.user.pk == self.kwargs["pk"]

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


class UserChangeAddressView(UserPassesTestMixin, View):
    def test_func(self):
        # Prevents the user from changing other users addresses
        return self.request.user.is_authenticated and self.request.user.pk == self.kwargs["pk"]

    def get(self, request, *args, **kwargs):
        user_pk = kwargs.get("pk")
        user = User.objects.get(pk=user_pk)
        form = UserAddressForm(instance=user.address)
        return render(request, "dating/change_address.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user_pk = kwargs.get("pk")
            user = User.objects.get(pk=user_pk)

            cd = form.cleaned_data
            street = cd.get("street")
            city = cd.get("city")
            post_code = cd.get("post_code")

            try:
                address = Address.objects.get(street=street, city=city, post_code=post_code)
                user.address = address  # Update user's address if it already exists in the database
                user.save()
                return redirect("settings", user.pk)
            except ObjectDoesNotExist:  # Create a new address if it doesn't exist in the database
                address = Address.objects.create(street=street, city=city, post_code=post_code)
                user.address = address
                user.save()
                return redirect("settings", user.pk)
        return render(request, "dating/change_address.html", context={"form": form})


class MeetingListView(ListView):
    model = Meeting
    template_name = "dating/meetings.html"
    context_object_name = "meetings"

    def get_queryset(self):
        return Meeting.objects.filter(participating_users=self.request.user).order_by("date", "time")


class MeetingAddView(LoginRequiredMixin, FormView):
    form_class = MeetingAddForm
    template_name = "dating/create_meeting.html"
    success_url = reverse_lazy("meetings")

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields["participating_dogs"].limit_choices_to = {"owner": self.request.user}
        return modelform

    def form_valid(self, form):
        cd = form.cleaned_data

        # Meeting form data
        date = cd.get("date")
        time = cd.get("time")
        max_users = cd.get("max_users")
        max_dogs = cd.get("max_dogs")
        target_user_gender = cd.get("target_user_gender")
        target_user_age = cd.get("target_user_age")
        target_dog_sex = cd.get("target_dog_sex")
        target_dog_age = cd.get("target_dog_age")
        notes = cd.get("notes")
        participating_dogs = cd.get("participating_dogs")

        # Address form data
        street = cd.get("street")
        city = cd.get("city")
        post_code = cd.get("post_code")

        # Search the database if address already exists
        try:
            address = Address.objects.get(street=street, city=city, post_code=post_code)

        # Create a new address if it doesn't exist in the database
        except ObjectDoesNotExist:
            address = Address.objects.create(street=street, city=city, post_code=post_code)

        meeting = Meeting.objects.create(
            date=date,
            time=time,
            max_users=max_users,
            max_dogs=max_dogs,
            target_user_gender=target_user_gender,
            target_user_age=target_user_age,
            target_dog_sex=target_dog_sex,
            target_dog_age=target_dog_age,
            address=address,
            notes=notes,
            created_by=self.request.user,
        )
        meeting.participating_dogs.set(participating_dogs)
        meeting.participating_users.add(self.request.user)
        return super().form_valid(form)


class MeetingDetailsView(LoginRequiredMixin, DetailView):
    context_object_name = "meeting"
    model = Meeting
    template_name = "dating/meeting_details.html"


class MeetingUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # Prevents the user from editing meetings they didn't create
        meeting_creator = Meeting.objects.get(pk=self.kwargs["pk"]).created_by
        return self.request.user.is_authenticated and self.request.user == meeting_creator

    context_object_name = "meeting"
    model = Meeting
    template_name = "dating/edit_meeting.html"
    form_class = MeetingAddForm
    success_url = reverse_lazy("meetings")

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields["participating_dogs"].limit_choices_to = {"owner": self.request.user}
        return modelform

    def form_valid(self, form):
        other_users_dogs = list(self.object.participating_dogs.all().exclude(owner=self.request.user))
        response = super().form_valid(form)
        [self.object.participating_dogs.add(dog) for dog in other_users_dogs]
        return response

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        # Pass meeting address instance to form
        meeting_address = {
            "street": self.object.address.street,
            "post_code": self.object.address.post_code,
            "city": self.object.address.city,
        }
        self.initial.update(meeting_address)
        return self.initial.copy()


class MeetingDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        # Prevents the user from deleting meetings they didn't create
        meeting_creator = Meeting.objects.get(pk=self.kwargs["pk"]).created_by
        return self.request.user.is_authenticated and self.request.user == meeting_creator

    model = Meeting
    template_name = "dating/delete_meeting.html"
    success_url = reverse_lazy("meetings")


class MeetingSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = MeetingSearchForm()
        return render(request, "dating/meetings_search.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = MeetingSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            city = cd.get("city")
            date = cd.get("date")
            target_user_gender = cd.get("target_user_gender")
            max_users = cd.get("max_users")
            max_dogs = cd.get("max_dogs")

            # Mandatory fields search results
            meetings = Meeting.objects.filter(address__city__icontains=city,
                                              date__gte=date,
                                              created_by__gender=target_user_gender
                                              ).order_by("date", "time")
            # Additional fields filters
            if max_users and max_dogs:
                meetings = meetings.filter(max_users__lte=max_users, max_dogs__lte=max_dogs).order_by(
                    "-max_users", "-max_dogs")
            elif max_users:
                meetings = meetings.filter(max_users__lte=max_users).order_by("-max_users")
            elif max_dogs:
                meetings = meetings.filter(max_dogs__lte=max_dogs).order_by("-max_dogs")

            context = {
                "form": form,
                "meetings": meetings,
            }
            return render(request, "dating/meetings_search.html", context)
        return render(request, "dating/meetings_search.html", {"form": form})


class MeetingJoinView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        # Prevents the user from joining the meetings they created
        meeting_creator = Meeting.objects.get(pk=self.kwargs["pk"]).created_by
        return self.request.user.is_authenticated and self.request.user != meeting_creator

    form_class = MeetingJoinForm
    model = Meeting
    template_name = "dating/meeting_join.html"
    success_url = reverse_lazy("meetings")

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields["participating_dogs"].limit_choices_to = {"owner": self.request.user}
        return modelform

    def form_valid(self, form):
        meeting_creator_dogs = list(self.object.participating_dogs.filter(owner=self.object.created_by))
        response = super().form_valid(form)
        self.object.participating_users.add(self.request.user)
        [self.object.participating_dogs.add(dog) for dog in meeting_creator_dogs]
        return response


class SearchProfilesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = SearchProfilesForm()
        return render(request, "dating/search_profiles.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SearchProfilesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            query = cd.get("query")

            # Search for users
            usernames = User.objects.filter(username__icontains=query)
            first_names = User.objects.filter(first_name__icontains=query)
            last_names = User.objects.filter(last_name__icontains=query)
            user_profiles = usernames | first_names | last_names

            # Search for dogs
            dog_names = Dog.objects.filter(name__icontains=query)
            dog_breeds = Dog.objects.filter(breed__icontains=query)
            dog_profiles = dog_names | dog_breeds

            context = {
                "form": form,
                "user_profiles": user_profiles,
                "dog_profiles": dog_profiles,
            }

            return render(request, "dating/search_profiles.html", context)
        return render(request, "dating/search_profiles.html", {"form": form})
