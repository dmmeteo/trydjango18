from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
import django_couch
from .forms import FiltersForm

# Declare our database source
db = django_couch.db('db')


def home(request):
    return render(request, 'filters/home.html', {})


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
            "word": str(word)
        })

        # Create our document
        db.create(data)

        messages.success(request, 'You have successfully created a new filter, {}' .format(request.user))
        return redirect('filters:home')

    return render(request, 'filters/add.html', {'form': form})


def conf(request):
    return render(request, 'filters/filters_config.html', {})
