from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from .forms import ThreadCreateForm, MessageForm
from .models import Thread, Message

User = get_user_model()


class ThreadsList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        context = {
            "threads": threads,
        }
        return render(request, "user_messages/inbox.html", context)


class ThreadCreate(LoginRequiredMixin, View):
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
                    return redirect("thread", pk=thread.pk)
                elif Thread.objects.filter(sender=recipient, recipient=request.user).exists():
                    thread = Thread.objects.filter(sender=recipient, recipient=request.user).first()
                    return redirect("tread", pk=thread.pk)

                thread = Thread.objects.create(sender=request.user, recipient=recipient)
                return redirect("thread", pk=thread.pk)
            except ObjectDoesNotExist:
                messages.error(request, f"Nie znaleziono użytkownika {username}")
                return redirect("create-thread")


class ThreadView(UserPassesTestMixin, View):
    def test_func(self):
        # Prevents the user from viewing other users threads
        thread = Thread.objects.get(pk=self.kwargs["pk"])
        return self.request.user.is_authenticated and\
               self.request.user == thread.sender or\
               self.request.user == thread.recipient

    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = Thread.objects.get(pk=pk)
        message_list = Message.objects.filter(thread__pk__contains=pk).order_by("date")
        context = {
            "form": form,
            "thread": thread,
            "message_list": message_list,
        }
        for message in message_list:
            if message.sender_user != request.user:
                message.is_read = True
                message.save()
        return render(request, "user_messages/thread.html", context)


class MessageCreate(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        thread = Thread.objects.get(pk=pk)
        if thread.recipient == request.user:
            recipient = thread.sender
        else:
            recipient = thread.recipient
        message = Message.objects.create(
            thread=thread,
            sender_user=request.user,
            recipient_user=recipient,
            content=request.POST.get("message")
        )
        return redirect("thread", pk)
