from django.shortcuts import render
from .forms import CouchForm
import django_couch
from django.shortcuts import redirect
from django.utils import timezone


# Create your views here.
def home(request):

    # Added our form.
    form = CouchForm(request.POST or None)

    # Define a couchdb source
    db = django_couch.db('db')

    # Create a document in couchdb
    # data = {"source": {"title": "Django", "link": "http://djangoproject.com"}, "type": "subscriptions"}
    # result = db.create(data)

    # Fetching a data from couchdb.
    query = db.view('sub/sub').rows

    # Checking a form
    if form.is_valid():
        title = form.cleaned_data.get('title')
        link = form.cleaned_data.get('link')

        # Sending our data to the couchdb
        data = {"title": title, "link": link, "type": "subscriptions"}

        # Create our document in couchdb
        db.create(data)
        return redirect('couch:home')

    # Define our context, that we'll send.
    context = {
        'form': form,
        # 'result': result,
        'query': query
    }

    return render(request, 'couch/home.html', context)
