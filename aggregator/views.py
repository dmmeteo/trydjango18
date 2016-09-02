from django.contrib import messages
from .forms import AddRssSource, FiltersForm
from django.shortcuts import redirect
import feedparser
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to


# Simple view, that list whole specter rss source.
@login_required()
@render_to('aggregator/home_source.html')
def home_aggregator(request):
    # Get our view from couch, set it to response variable and represent it likes rows
    response = request.db.view('subscriptions/source', key=str(request.user)).rows

    # Save all rows
    items = []
    # Pass through loop all couch rows and append it into items
    for item in response:
        items.append(item)

    # Return our rendered template with reverse sorting a couch view
    return {'response': sorted(items, reverse=True)}


# The view that check our form and create a new document each time, when we sent post data by means the form
@login_required()
@render_to('aggregator/add_source.html')
def aggregator_actions(request, doc_id=None):
    # Get our view from couch, set it to response variable and represent it likes rows
    response = request.db.view('subscriptions/sorted_source', key=doc_id).rows

    # Declare our form for adding new rss sources
    form = AddRssSource(request.POST or None)

    # If we have got a doc id, we'll proceed.
    if doc_id:
        # Save title and link into items list
        items = []

        # Looping all values, and if our doc_id in loop, we're adding elements into list
        for item in response:
            for val in item.value[0:2]:
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
            # This data will be written into chouchrequest.db document
            changed_data = form.cleaned_data

            # Here's starting write process the updated document into couch
            rss_source = request.db[doc_id]
            rss_source.update(changed_data)
            rss_source.save()

            # Show success message after all
            messages.success(request, 'You have successfully changed data of the source.')
            return redirect('edit_source')
    else:
        # Data that must to be send by means form in couch
        data = {
            "user": str(request.user),
            "read": False,
            "type": "source"
        }

        # Checking our form
        if form.is_valid():
            # Data that must to be send by means form in couch
            data.update(form.cleaned_data)
            request.db.create(data)

            # Send a success message.
            messages.success(request, 'You have successfully added a new source.')
            return redirect('home_source')

    return {'form': form}


# The edit view deletes unneeded sources and show all available sources for certain user
@login_required()
@render_to('aggregator/edit_source.html')
def edit_aggregator(request):
    # Get our view from couch, set it to response variable and represent it likes rows
    response = request.db.view('subscriptions/source', key=str(request.user)).rows

    # Define our empty list for values from couch
    items = []

    # Pass all keys through loop
    for item in response:
        items.append(item)

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couch by means loop
    if 'on_delete' in request.POST:
        for item in checkboxes:
            request.db.delete(request.db[item])

        # Send an info message, if post doesn't empy.
        if 'item' in request.POST:
            messages.success(request, 'You have successfully deleted sources.')
        return redirect('edit_source')
    # In another case we just mark all selected sources as read
    elif 'as_read' in request.POST:
        for value in checkboxes:
            # Update our documents in couch
            doc = {"read": True}
            rss_source = request.db[value]
            rss_source.update(doc)
            rss_source.save()

        # Print out success message, if post doesn't empty
        if 'item' in request.POST:
            messages.success(request, 'You have successfully marked as read the source.')
        return redirect('edit_source')

    # Return our rendered template with reverse sorting a couch view
    return {'response': sorted(items, reverse=True)}


# The parse view is retrieving whole bunch of stuff from rss feeds
@login_required()
@render_to('aggregator/parse_source.html')
def parse_aggregator(request, doc_id):
    # Get our view from couch, set it to response variable and represent it likes rows
    response = request.db.view('subscriptions/sorted_source', key=doc_id).rows

    # Save title and link into items list
    items = []

    # Retrieving title and link of a couch document and write it into items list
    for item in response:
            items.append(item.value[0])
            items.append(item.value[1])

    # Set a link, that will be parsed
    source = feedparser.parse(items[1])

    # Define our list and dict in context
    context = {
        'items': items,
        'source': source
    }

    return context


# List all available filters for user, that will be parsed
@login_required()
@render_to('aggregator/home_filter.html')
def home_filter(request):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/filter', key=str(request.user)).rows

    # Save all available filters for certain user into list
    items = []

    for item in response:
            items.append(item)

    return {'response': sorted(items, reverse=True)}


# Add a new filter view
@login_required()
@render_to('aggregator/filter_actions.html')
def filter_actions(request, doc_id=None):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/sorted_filter', key=doc_id).rows

    # Retrieving a FiltersForm
    form = FiltersForm(request.POST or None)

    # Save title, item, action, word and link in this list.
    items = []

    # If we have got a doc id, we'll proceed.
    if doc_id:
        for item in response:
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

        # If everything is alright with our form, we'll write these shit straight into couch.
        if form.is_valid():
            changed_data = form.cleaned_data

            # Update our doc
            rss_filter = request.db[doc_id]
            rss_filter.update(changed_data)
            rss_filter.save()

            messages.info(request, 'Successfully updated.')
            return redirect('conf_filter')
    else:
        # Write down a user name and a type of couch document
        data = {
            "user": str(request.user),
            "type": "filter"
        }

        if form.is_valid():
            # After successful checking of conditions, write down into data's dict title and word from post request
            data.update(form.cleaned_data)

            # Create our document
            request.db.create(data)

            messages.success(request, 'You have successfully created a new filter, {}'.format(request.user))
            return redirect('home_filter')

    return {'form': form}


# Simple configuration of filters, that will be parsed
@login_required()
@render_to('aggregator/filters_config.html')
def conf_filter(request):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/filter', key=str(request.user)).rows

    # Save all users' filters into list
    items = []

    for item in response:
        items.append(item)

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couch by means loop
    if 'button' in request.POST:
        for item in checkboxes:
            request.db.delete(request.db[item])

        # Send an info message, if post doesn't empty.
        if 'item' in request.POST:
            messages.info(request, 'You have successfully deleted filters.')
        return redirect('home_filter')

    return {'response': sorted(items, reverse=True)}


# The filter parser is a view, that parse a rss feed by certain rules.
@login_required()
@render_to('aggregator/parser_filter.html')
def parser_filter(request, doc_id):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/sorted_filter', key=doc_id).rows

    # Save all filters into item's list
    items = []

    for item in response:
        for value in item.value:
            items.append(value)

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
