from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
import django_couch
from .forms import FiltersForm
import feedparser

# Declare our database source
db = django_couch.db('db')


# List all available filters for user, that will be parsed
def home(request):
    # Retrieving all filter's documents from couchdb
    response = db.view('subscriptions/filter').rows

    # Save all available filters for certain user into list
    items = []

    for foo in response:
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


def conf(request):
    # Retrieving our filter view from couchdb
    response = db.view('subscriptions/filter').rows

    # Save all users' filters into list
    items = []

    for foo in response:
        if foo.key == str(request.user):
            items.append(foo)

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couchdb by means loop
    if 'button' in request.POST:
        for foo in checkboxes:
            db.delete(db[foo])

        # Send an info message, if post doesn't empy.
        if 'item' in request.POST:
            messages.info(request, 'You have successfully deleted filters.')
        return redirect('filters:conf')

    return render(request, 'filters/filters_config.html', {'response': sorted(items)})


def filter_parser(request, doc_id):
    # Retrieving filter's view from couchdb
    response = db.view('subscriptions/filter').rows

    # Save all filters into item's list
    items = []

    for foo in response:
        if doc_id == foo.id:
            items.append(foo.value)

    # Parse this source
    source = feedparser.parse(items[0][4])

    # Parsed values (title, description) will be saved here.
    parsed = []

    # Staring parsing
    for bar in source.entries:
        # If word in title and item is title, and action is "contains",
        # we'll write all matched values into parsed list
        if items[0][3] in bar.title and (int(items[0][1]) is 1 and int(items[0][2]) is 1):
            if str(items[0][3]).islower() or str(items[0][3]).istitle():
                parsed.append(bar)

        # If word in description and item is title, and action is "contains",
        # we'll write all matched values into parsed list
        elif items[0][3] in bar.description and (int(items[0][1]) is 2 and int(items[0][2]) is 1):
            if str(items[0][3]).islower() or str(items[0][3]).istitle():
                parsed.append(bar)

        # If word in title and item is title, and action is "don't contain",
        # we'll write all matched values into parsed list
        elif not items[0][3] in bar.title and (int(items[0][1]) is 1 and int(items[0][2]) is 2):
            if str(items[0][3]).islower() or str(items[0][3]).istitle():
                parsed.append(bar)

        # If word in description and item is title, and action is "don't contain",
        # we'll write all matched values into parsed list
        elif not items[0][3] in bar.description and (int(items[0][1]) is 2 and int(items[0][2]) is 2):
            if str(items[0][3]).islower() or str(items[0][3]).istitle():
                parsed.append(bar)

    return render(request, 'filters/parser.html', {'response': parsed, 'title': items[0][0]})
