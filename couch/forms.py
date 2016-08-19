from django import forms


# Create a form with two fields, that both are required with max length 255 symbols.
class CouchForm(forms.Form):
    title = forms.CharField(required=True, max_length=255)
    link = forms.CharField(required=True, max_length=255)
