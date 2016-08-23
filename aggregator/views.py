from django.contrib import messages
from django.shortcuts import render
from .forms import AddRssSource
from django.shortcuts import redirect
import django_couch
import datetime

# Declare our couch database source
db = django_couch.db('db')


# Simple view, that list whole specter rss source.
def home(request):
    # Get our view from couchdb, set it to response variable and represent it likes rows
    response = db.view('subscriptions/source').rows

    # Return our rendered template with reverse sorting a couch view
    return render(request, 'aggregator/home.html', {'response': sorted(response, reverse=True)})


# The view that check our form and create a new document each time, when we sent post data by means the form
def add(request):
    # Declare our form for adding new rss sources
    form = AddRssSource(request.POST or None)

    # Checking our form
    if form.is_valid():
        title = form.cleaned_data.get('title')
        link = form.cleaned_data.get('link')

        # Data that must to be send by means form in chouchdb
        data = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "title": title, "link": link,
                "user": str(request.user), "read": False,
                "type": "source"}
        db.create(data)

        # Send a success message.
        messages.success(request, 'You have successfully added a new source.')
        return redirect('aggregator:home')

    return render(request, 'aggregator/add.html', {'form': form})


# Edit view deletes unneeded sources and show all available sources for certain user
def edit(request):
    # Get our view from couchdb, set it to response variable and represent it likes rows
    response = db.view('subscriptions/source').rows

    # Define our empty list for values from couchdb
    items = []

    # Pass all keys though loop
    for key in response:
        if str(request.user) == key.value[2]:
            items.append(key)

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couchdb by means loop
    if 'on_delete' in request.POST:
        for foo in checkboxes:
            db.delete(db[foo])

        # Send an info message.
        messages.success(request, 'You have successfully deleted the source.')
        return redirect('aggregator:edit')
    # In another case we just mark it as read sources
    # elif 'as_read' in request.POST:
    #     for bar in checkboxes:
    #         db.update(db)


    # Return our rendered template with reverse sorting a couch view
    return render(request, 'aggregator/edit.html', {'response': sorted(items, reverse=True)})


def update(request):
    return render(request, 'aggregator/update.html', {})
