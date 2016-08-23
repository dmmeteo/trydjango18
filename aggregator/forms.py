from django import forms
from django.forms.extras.widgets import SelectDateWidget


# Add a simple form for opportunity creating new rss sources, that must to be parsed.
class AddRssSource(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    link = forms.CharField(max_length=500, required=True)
