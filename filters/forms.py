from django import forms

# Define our choices for filter's form
items = (
    ('title', 'Title'),
    ('desc', 'Description')
)

actions = (
    ('contains', 'Contains'),
    ('dc', 'Don\'t contain')
)


# FiltersForm is print out title, two select elements and an one required textinput's field
class FiltersForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A title'}), label='Title')
    item = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker'}), required=False, label='If',
                             choices=items)
    action = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker'}), required=False, label='is',
                               choices=actions)
    word = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'a word'}))
    link = forms.URLField(max_length=255, widget=forms.URLInput(attrs={'value': 'http://'}))
