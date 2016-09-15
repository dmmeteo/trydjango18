from django.contrib import messages
from .forms import AddRssSource, FiltersForm
from django.shortcuts import redirect
import feedparser
# Using of login_required
from django.contrib.auth.decorators import login_required
# Using of render_to
from annoying.decorators import render_to
from django.http import Http404
from django_couch import ResourceNotFound


# Simple view, that list whole specter rss source.
@login_required()
@render_to('aggregator/home_source.html')
def home_aggregator(request):
    # Get our view from couch, set it to response variable and represent it likes rows
    response = request.db.view('subscriptions/sources', key=str(request.user)).rows

    # Return our rendered template with reverse sorting a couch view
    return {'response': sorted(response, reverse=True)}


# The view that check our form and create a new document each time, when we sent post data by means the form
@login_required()
@render_to('aggregator/add_source.html')
def aggregator_actions(request, doc_id=None):
    # Get our view from couch, set it to response variable and represent it likes rows
    # Correct feting of documents from couchdb
    response = request.db.view('subscriptions/form_source', key=doc_id).rows

    # Declare our form for adding new rss sources
    form = AddRssSource(request.POST or None)

    # If we have got a doc id, we'll proceed.
    if doc_id:
        # Save title and link into items list
        values = {}

        # Looping all values, and if our doc_id in loop, we're adding elements into list
        for item in response:
                values.update(item.value)

        # Define the form with initial data
        form = AddRssSource(request.POST or None, initial=values)

        # Validate our form
        if form.is_valid():
            # This data will be written into couch document, using form.cleaned_data for update
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
    response = request.db.view('subscriptions/sources', key=str(request.user)).rows

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couch by means loop
    if 'on_delete' in request.POST:
        for item in checkboxes:
            try:
                request.db.delete(request.db[item])
            except ResourceNotFound:
                raise Http404

        # Send an info message, if post doesn't empty.
        if 'item' in request.POST:
            messages.success(request, 'You have successfully deleted sources.')
        return redirect('edit_source')
    # In another case we just mark all selected sources as read
    elif 'as_read' in request.POST:
        for value in checkboxes:
            # Update our documents in couch
            doc = {"read": True}
            try:
                rss_source = request.db[value]
                rss_source.update(doc)
                rss_source.save()
            except ResourceNotFound:
                raise Http404

        # Print out success message, if post doesn't empty
        if 'item' in request.POST:
            messages.success(request, 'You have successfully marked as read the source.')
        return redirect('edit_source')

    # Return our rendered template with reverse sorting a couch view
    return {'response': sorted(response, reverse=True)}


# The parse view is retrieving whole bunch of stuff from rss feeds
@login_required()
@render_to('aggregator/parse_source.html')
def parse_aggregator(request, doc_id):
    # Get our view from couch, set it to response variable and represent it likes rows
    response = request.db.view('subscriptions/sorted_source', key=doc_id).rows

    # Save title and link into items list
    values = {}

    # Retrieving title and link of a couch document and write it into items list
    for item in response:
        values.update(item.value)

    # Set a link, that will be parsed
    source = feedparser.parse(values['link'])

    # Define our list and dict in context
    context = {
        'items': values,
        'source': source
    }

    return context


# Filter's views
# List all available filters for user, that will be parsed
@login_required()
@render_to('aggregator/home_filter.html')
def home_filter(request):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/filters', key=str(request.user)).rows

    return {'response': sorted(response, reverse=True)}


# Add a new filter view in another case just update it
@login_required()
@render_to('aggregator/filter_actions.html')
def filter_actions(request, doc_id=None):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/sorted_filter', key=doc_id).rows

    # Save title, item, parsed, word and link in this dict.
    values = {}

    # If we have got a doc id, we'll proceed.
    if doc_id:
        for item in response:
            values.update(item.value)

        # Declare our form
        form = FiltersForm(request.POST or None, initial=values, db=request.db, user=request.user)

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
        # Retrieving a FiltersForm
        form = FiltersForm(request.POST or None, db=request.db, user=request.user)

        # Refactoring of filter_add
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
    response = request.db.view('subscriptions/filters', key=str(request.user)).rows

    # Save all selected checkboxes in variable
    checkboxes = request.POST.getlist('item')

    # All selected values we're deleting from couch by means loop
    if 'button' in request.POST:
        for item in checkboxes:
            try:
                request.db.delete(request.db[item])
            except ResourceNotFound:
                raise Http404

        # Send an info message, if post doesn't empty.
        if 'item' in request.POST:
            messages.info(request, 'You have successfully deleted filters.')
        return redirect('home_filter')

    return {'response': sorted(response, reverse=True)}


# The filter parser is a view, that parse a rss feed by certain rules.
@login_required()
@render_to('aggregator/parser_filter.html')
def parser_filter(request, doc_id):
    # Catch up all documents that satisfied our couch view
    response = request.db.view('subscriptions/sorted_filter', key=doc_id).rows

    # Save all filters into item's list
    values = response[0].value

    # Here we're saving parsed links of our sources.
    links = []
    for source in values['sources']:
        try:
            # We're parsing whole bunch of links that located in filter of user.
            links.append(feedparser.parse(request.db[source].link))
        except ResourceNotFound:
            pass

    # Save filtered sources
    parsed_result = []

    # Deleted magic indexes
    for link in links:
        for parsed in link.entries:
            title, description, word = parsed.title.lower(), parsed.description.lower(), values['word'].lower()
            val1, val2 = str(values['item']), str(values['action'])

            # If word in title and item is title, and parsed is "contains",
            # we'll write all matched values into parsed list
            if word in title and ('title' in val1 and 'contains' in val2):
                parsed_result.append(parsed)

            # If word in description and item is title, and parsed is "contains",
            # we'll write all matched values into parsed list
            elif word in description and ('desc' in val1 and 'contains' in val2):
                parsed_result.append(parsed)

            # If word in title and item is title, and parsed is "don't contain",
            # we'll write all matched values into parsed list
            elif word not in title and ('title' in val1 and 'dc' in val2):
                parsed_result.append(parsed)

            # If word in description and item is title, and parsed is "don't contain",
            # we'll write all matched values into parsed list
            elif word not in description and ('desc' in val1 and 'dc' in val2):
                parsed_result.append(parsed)

    return {'response': parsed_result, 'title': values['title']}
