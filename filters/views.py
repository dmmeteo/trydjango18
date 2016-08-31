from django.contrib import messages
from django.shortcuts import redirect
from .forms import FiltersForm
import feedparser
from rss_aggregator.connetction import db, response
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to


# List all available filters for user, that will be parsed
@login_required()
@render_to('filters/home.html')
def home(request):
    # Save all available filters for certain user into list
    items = []

    for foo in response('filter'):
        if foo.key == str(request.user):
            items.append(foo)

    return {'response': sorted(items, reverse=True)}


# Add a new filter view
@login_required()
@render_to('filters/add.html')
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
        print data

        messages.success(request, 'You have successfully created a new filter, {}'.format(request.user))
        return redirect('filters:home')

    return {'form': form}


# Simple configuration of filters, that will be parsed
@login_required()
@render_to('filters/filters_config.html')
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

    return {'response': sorted(items)}


# The filter parser is a view, that parse a rss feed by certain rules.
@login_required()
@render_to('filters/parser.html')
def filter_parser(request, doc_id):
    # Save all filters into item's list
    items = []

    for foo in response('filter'):
        if doc_id == foo.id:
            for val in foo.value:
                items.append(val)

    # Parse this source
    source = feedparser.parse(items[4])

    # Parsed values (title, description) will be saved here.
    parsed = []

    # Staring parsing
    for bar in source.entries:
        # Define our variables
        title, description, word = bar.title.lower(), bar.description.lower(), items[3].lower()
        val1, val2 = str(items[1]), str(items[2])

        # If word in title and item is title, and action is "contains",
        # we'll write all matched values into parsed list
        if word in title and ('title' in val1 and 'contains' in val2):
                parsed.append(bar)

        # If word in description and item is title, and action is "contains",
        # we'll write all matched values into parsed list
        elif word in description and ('desc' in val1 and 'contains' in val2):
                parsed.append(bar)

        # If word in title and item is title, and action is "don't contain",
        # we'll write all matched values into parsed list
        elif word not in title and ('title' in val1 and 'dc' in val2):
                parsed.append(bar)

        # If word in description and item is title, and action is "don't contain",
        # we'll write all matched values into parsed list
        elif word not in description and ('desc' in val1 and 'dc' in val2):
                parsed.append(bar)

    return {'response': parsed, 'title': items[0]}


# Update view
@login_required()
@render_to('filters/update.html')
def update(request, doc_id):

    # Save title, item, action, word and link in this list.
    items = []

    for foo in response('filter'):
        if doc_id in foo.id:
            for val in foo.value:
                items.append(val)

    # Initial data for form
    data = {
        'title': items[0],
        'item': items[1],
        'action': items[2],
        'word': items[3],
        'link': items[4]
    }

    # Declare our form
    form = FiltersForm(request.POST or None, initial=data)

    # If everything is alright with our form, we'll write these shit straight into couchdb.
    if form.is_valid():
        changed_data = form.cleaned_data

        # print dict

        # Update our doc
        doc_update = db[doc_id]
        doc_update.update(changed_data)
        doc_update.save()

        messages.info(request, 'Successfully updated.')
        return redirect('filters:conf')

    return {'form': form}
