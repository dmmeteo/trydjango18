from django.shortcuts import render
from . import forms
import django_couch


# Create your views here.
def home(request):

    # Added our form.
    form = forms.CouchForm

    # Define a couchdb source
    db = django_couch.db('db')

    # Create a document in couchdb
    # data = {"source": {"title": "Django", "link": "http://djangoproject.com"}, "type": "subscriptions"}
    # result = db.create(data)

    # Fetching a data from couchdb.
    query = db.view('sub/subs').rows

    # Define our context, that we'll send.
    context = {
        'form': form,
        # 'result': result,
        'query': query
    }

    return render(request, 'couch/home.html', context)
