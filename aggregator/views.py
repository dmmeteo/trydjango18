from django.shortcuts import render
from .forms import AddRssSource
from django.shortcuts import redirect
import django_couch
import datetime

# Declare our couch database source
db = django_couch.db('db')


def home(request):
    return render(request, 'aggregator/home.html', {})


# The view that check our form and create a new document each time, when we sent post data by means the form
def add(request):
    # Declare our form for adding new rss sources
    form = AddRssSource(request.POST or None)

    # Checking our form
    if form.is_valid():
        title = form.cleaned_data.get('title')
        link = form.cleaned_data.get('link')

        # Data that must to be send
        data = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "title": title, "link": link,
                "type": "source"}
        db.create(data)
        return redirect('aggregator:home')

    return render(request, 'aggregator/add.html', {'form': form})


def edit(request):
    return render(request, 'aggregator/edit.html', {})
