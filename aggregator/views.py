from django.contrib import messages
from django.shortcuts import render
from .forms import AddRssSource
from django.shortcuts import redirect
import datetime
import feedparser
from django.contrib.auth.decorators import login_required
from rss_aggregator.connetction import db, response


# Simple view, that list whole specter rss source.
@login_required()
def home(request):
    # Save all rows
    items = []

    # Pass through loop all couchdb rows and append it into items
    for foo in request.db('db').views('subscriptions/source'):
        if str(request.user) == foo.value[2]:
            items.append(foo)

    # Return our rendered template with reverse sorting a couch view
    return render(request, 'aggregator/home.html', {'response': sorted(items, reverse=True)})


# The view that check our form and create a new document each time, when we sent post data by means the form
@login_required()
def add(request):
    # Declare our form for adding new rss sources
    form = AddRssSource(request.POST or None)

    # Checking our form
    if form.is_valid():
        # Data that must to be send by means form in chouchdb
        data = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": form.cleaned_data.get('title'),
            "link": form.cleaned_data.get('link'),
            "user": str(request.user),
            "read": False,
            "type": "source"
        }
        db.create(data)

        # Send a success message.
        messages.success(request, 'You have successfully added a new source.')
        return redirect('aggregator:home')

    return render(request, 'aggregator/add.html', {'form': form})


# The edit view deletes unneeded sources and show all available sources for certain user
@login_required()
def edit(request):
    # Define our empty list for values from couchdb
    items = []

    # Pass all keys through loop
    for foo in response('source'):
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
            messages.success(request, 'You have successfully deleted sources.')
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
@login_required()
def update(request, doc_id):
    # Save title and link into items list
    items = []

    # Looping all values, and if our doc_id in loop, we're adding elements into list
    for foo in response('source'):
        if doc_id in foo.id:
            for val in foo.value[0:2]:
                items.append(val)

    # Initial data for our form
    data = {
        'title': items[0],
        'link': items[1]
    }

    # Define the form with initial data
    form = AddRssSource(request.POST or None, initial=data)

    # Validate our form
    if form.is_valid():
        # This data will be written into chouchdb document
        changed_data = form.cleaned_data

        # Here's starting write process the updated document into couchdb
        result = db[doc_id]
        result.update(changed_data)
        result.save()

        # Show success message after all
        messages.success(request, 'You have successfully changed data of the source.')
        return redirect('aggregator:edit')

    return render(request, 'aggregator/update.html', {'form': form})


# The parse view is retrieving whole bunch of stuff from rss feeds
@login_required()
def parse(request, doc_title):
    # Save title and link into items list
    items = []

    # Retrieving title and link of a couchdb document and write it into items list
    for foo in response('source'):
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
