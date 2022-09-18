from django.shortcuts import render
from django.views import View


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "base.html")


class AboutAppView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dating/about.html")
