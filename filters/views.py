from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import FiltersForm
import feedparser
from rss_aggregator.connetction import db, response


# List all available filters for user, that will be parsed
def home(request):
    # Save all available filters for certain user into list
    items = []

    for foo in response('filter'):
        if foo.key == str(request.user):
            items.append(foo)

    return render(request, 'filters/home.html', {'response': sorted(items, reverse=True)})


# Add a new filter view
def add(request):
    # Retrieving a FiltersForm
    form = FiltersForm(request.POST or None)

    # Write down a user name and a type of couch document
    data = {
        "user": str(request.user),
        "type": "filter"
    }

    if form.is_valid():
        # After successful checking of conditions, write down into data's dict title and word from post request
        data.update(form.cleaned_data)

        # Create our document
        db.create(data)

        messages.success(request, 'You have successfully created a new filter, {}'.format(request.user))
        return redirect('filters:home')

    return render(request, 'filters/add.html', {'form': form})


# Simple configuration of filters, that will be parsed
def conf(request):
    # Save all users' filters into list
    items = []

    for foo in response('filter'):
        if foo.key == str(request.user):
            items.append(foo)

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couchdb by means loop
    if 'button' in request.POST:
        for foo in checkboxes:
            db.delete(db[foo])

        # Send an info message, if post doesn't empty.
        if 'item' in request.POST:
            messages.info(request, 'You have successfully deleted filters.')
        return redirect('filters:home')

    return render(request, 'filters/filters_config.html', {'response': sorted(items)})


# The filter parser is a view, that parse a rss feed by certain rules.
def filter_parser(request, doc_id):
    # Save all filters into item's list
    items = []

    for foo in response('filter'):
        if doc_id == foo.id:
            for val in foo:
                items.append(val)

    # Parse this source
    source = feedparser.parse(items[4])

    # Parsed values (title, description) will be saved here.
    parsed = []

    # Staring parsing
    for bar in source.entries:
        # Define our variables
        title, description, word = bar.title.lower(), bar.description.lower(), items[3].lower()
        val1, val2 = int(items[1]), int(items[2])

        # If word in title and item is title, and action is "contains",
        # we'll write all matched values into parsed list
        if word in title and (val1 is 1 and val2 is 1):
                parsed.append(bar)

        # If word in description and item is title, and action is "contains",
        # we'll write all matched values into parsed list
        elif word in description and (val1 is 2 and val2 is 1):
                parsed.append(bar)

        # If word in title and item is title, and action is "don't contain",
        # we'll write all matched values into parsed list
        elif word not in title and (val1 is 1 and val2 is 2):
                parsed.append(bar)

        # If word in description and item is title, and action is "don't contain",
        # we'll write all matched values into parsed list
        elif word not in description and (val1 is 2 and val2 is 2):
                parsed.append(bar)

    return render(request, 'filters/parser.html', {'response': parsed, 'title': items[0]})
