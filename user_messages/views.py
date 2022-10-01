from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from .forms import ThreadCreateForm
from .models import Thread, Message

User = get_user_model()


class ThreadsList(View):
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        context = {
            "threads": threads,
        }
        return render(request, "user_messages/inbox.html", context)


class ThreadCreate(View):
    def get(self, request, *args, **kwargs):
        form = ThreadCreateForm()
        return render(request, "user_messages/thread_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            try:
                recipient = User.objects.get(username=username)
                if Thread.objects.filter(sender=request.user, recipient=recipient).exists():
                    thread = Thread.objects.filter(sender=request.user, recipient=recipient).first()
                    return redirect("tread", pk=thread.pk)
                elif Thread.objects.filter(sender=recipient, recipient=request.user).exists():
                    thread = Thread.objects.filter(sender=recipient, recipient=request.user).first()
                    return redirect("tread", pk=thread.pk)

                thread = Thread.objects.create(sender=request.user, recipient=recipient)
                return redirect("thread", pk=thread.pk)
            except ObjectDoesNotExist:
                return redirect("create-thread")
