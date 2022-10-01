from django.db.models import Q
from django.shortcuts import render
from django.views import View

from .models import Thread, Message


class ThreadsList(View):
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        context = {
            "threads": threads,
        }
        return render(request, "user_messages/inbox.html", context)
