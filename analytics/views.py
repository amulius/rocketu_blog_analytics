from django.shortcuts import render
from analytics.models import Page


def home(request):
    data = {
        'locations': Page.objects.all()
    }
    return render(request, 'home_analytics.html', data)