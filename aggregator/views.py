from django.contrib import messages
from django.shortcuts import render
from .forms import AddRssSource
from django.shortcuts import redirect
import django_couch
import datetime
import feedparser

# Declare our couch database source
db = django_couch.db('db')


# Simple view, that list whole specter rss source.
def home(request):
    # Get our view from couchdb, set it to response variable and represent it likes rows
    response = db.view('subscriptions/source').rows

    # Save all rows
    items = []

    # Pass through loop all couchdb rows and append it into items
    for foo in response:
        if str(request.user) == foo.value[2]:
            items.append(foo)

    # Return our rendered template with reverse sorting a couch view
    return render(request, 'aggregator/home.html', {'response': sorted(items, reverse=True)})


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


# The edit view deletes unneeded sources and show all available sources for certain user
def edit(request):
    # Get our view from couchdb, set it to response variable and represent it likes rows
    response = db.view('subscriptions/source').rows

    # Define our empty list for values from couchdb
    items = []

    # Pass all keys through loop
    for foo in response:
        if str(request.user) == foo.value[2]:
            items.append(foo)


    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couchdb by means loop
    if 'on_delete' in request.POST:
        for foo in checkboxes:
            db.delete(db[foo])

        # Send an info message, if post doesn't empy.
        if 'item' in request.POST:
            messages.success(request, 'You have successfully deleted the source.')
        return redirect('aggregator:edit')
    # In another case we just mark all selected sources as read
    elif 'as_read' in request.POST:
        for bar in checkboxes:
            # Update our documents in couchdb
            doc = {"read": True}
            result = db[bar]
            result.update(doc)
            result.save()

        # Print out success message, if post doesn't empty
        if 'item' in request.POST:
            messages.success(request, 'You have successfully marked as read the source.')
        return redirect('aggregator:edit')

    # Return our rendered template with reverse sorting a couch view
    return render(request, 'aggregator/edit.html', {'response': sorted(items, reverse=True)})


# The update view does a bunch of stuff: accept doc_id (couchdb id of document), check the form,
# save changed into couchdb.
def update(request, doc_id):
    # Get a dict with values by means couchdb view
    response = db.view('subscriptions/source').rows

    # Save title and link into items list
    items = []

    # Looping all values, and if our doc_id in loop, we're adding elements into list
    for foo in response:
        if doc_id in foo.id:
            items.append(foo.value[0])
            items.append(foo.value[1])

    # Initial data for our form
    data = {'title': items[0], 'link': items[1]}

    # Define the form with initial data
    form = AddRssSource(request.POST or None, initial=data)

    # Validate our form
    if form.is_valid():
        title = form.cleaned_data.get('title')
        link = form.cleaned_data.get('link')

        # This data will be written into chouchdb document
        changed_data = {"title": title, "link": link}

        # Here's starting write process the updated document into couchdb
        result = db[doc_id]
        result.update(changed_data)
        result.save()

        # Show success message after all
        messages.success(request, 'You have successfully changed data of the source.')
        return redirect('aggregator:edit')

    return render(request, 'aggregator/update.html', {'form': form})


# The parse view is retrieving whole bunch of stuff from rss feeds
def parse(request, doc_title):
    # Get a dict with values by means couchdb view
    response = db.view('subscriptions/source').rows

    # Save title and link into items list
    items = []

    # Retrieving title and link of a couchdb document and write it into items list
    for foo in response:
        if doc_title in foo.id:
            items.append(foo.value[0])
            items.append(foo.value[1])

    # Set a link, that will be parsed
    source = feedparser.parse(items[1])

    # Define our list and dict in context
    context = {
        'items': items,
        'source': source
    }

    return render(request, 'aggregator/parse.html', context)

def filters(request):
    return render(request, 'aggregator/filters.html', {})