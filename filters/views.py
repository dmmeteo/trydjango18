from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import FiltersForm
import feedparser
from rss_aggregator.connetction import db, response
from django.contrib.auth.decorators import login_required


# List all available filters for user, that will be parsed
@login_required
def home(request):
    # Save all available filters for certain user into list
    items = []

    for item in response('filter'):
        if item.key == str(request.user):
            items.append(item)

    return render(request, 'filters/home.html', {'response': sorted(items, reverse=True)})


# Add a new filter view
@login_required
def add(request):
    # Retrieving a FiltersForm
    form = FiltersForm(request.POST or None)

    # Write down a user name and a type of couch document
    data = {
        "user": str(request.user),
        "type": "filter"
    }

    if form.is_valid():
        title = form.cleaned_data.get('title')
        item = form.cleaned_data.get('item')
        action = form.cleaned_data.get('action')
        word = form.cleaned_data.get('word')
        link = form.cleaned_data.get('link')

        # If select's option has value of output like as item 1 and action 1, write it down into data dict,
        # and the same for rest
        if int(item) is 1 and int(action) is 1:
            data.update({
                "item": "1",
                "action": "1"
            })
        elif int(item) is 2 and int(action) is 2:
            data.update({
                "item": "2",
                "action": "2"
            })
        elif int(item) is 1 and int(action) is 2:
            data.update({
                "item": "1",
                "action": "2"
            })
        elif int(item) is 2 and int(action) is 1:
            data.update({
                "item": "2",
                "action": "1"
            })
        else:
            messages.error(request, 'Something went wrong.')

        # After successful checking of conditions, write down into data's dict title and word from post request
        data.update({
            "title": str(title),
            "word": str(word),
            "link": str(link)
        })

        # Create our document
        db.create(data)

        messages.success(request, 'You have successfully created a new filter, {}'.format(request.user))
        return redirect('filters:home')

    return render(request, 'filters/add.html', {'form': form})


# Simple configuration of filters, that will be parsed
@login_required
def conf(request):
    # Save all users' filters into list
    items = []

    for item in response('filter'):
        if item.key == str(request.user):
            items.append(item)

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couchdb by means loop
    if 'button' in request.POST:
        for item in checkboxes:
            db.delete(db[item])

        # Send an info message, if post doesn't empty.
        if 'item' in request.POST:
            messages.info(request, 'You have successfully deleted filters.')
        return redirect('filters:home')

    return render(request, 'filters/filters_config.html', {'response': sorted(items)})


# The filter parser is a view, that parse a rss feed by certain rules.
@login_required
def filter_parser(request, doc_id):
    # Save all filters into item's list
    items = []

    for item in response('filter'):
        if doc_id == item.id:
            for val in item.value:
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


# Update view
@login_required
def update(request, doc_id):

    # Save title, item, action, word and link in this list.
    items = []

    for item in response('filter'):
        if doc_id in item.id:
            for val in item.value:
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
        changed_data = {
            'title': form.cleaned_data.get('title'),
            'item': form.cleaned_data.get('item'),
            'action': form.cleaned_data.get('action'),
            'word': form.cleaned_data.get('word'),
            'link': form.cleaned_data.get('link'),
        }

        # Update our doc
        rss_filter = db[doc_id]
        rss_filter.update(changed_data)
        rss_filter.save()

        messages.info(request, 'Successfully updated.')
        return redirect('filters:conf')

    return render(request, 'filters/update.html', {'form': form})
