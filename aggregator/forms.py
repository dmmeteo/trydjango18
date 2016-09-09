from django import forms


# Add a simple form for opportunity creating new rss sources, that must to be parsed.
class AddRssSource(forms.Form):
    title = forms.CharField(max_length=255)
    link = forms.CharField(max_length=500)


# Define our choices for filter's form
# Created readable choices
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
    def __init__(self, *args, **kwargs):
        db = kwargs.pop('db', None)
        user = kwargs.pop('user', None)
        response = db.view('subscriptions/sources', key=str(user)).rows
        super(FiltersForm, self).__init__(*args, **kwargs)
        self.fields['sources'] = forms.MultipleChoiceField(
            widget=forms.SelectMultiple(attrs={'placeholder': 'Choose something'}),
            choices=[
                (item.id, item.value['title']) for item in response
                ])

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A title'}), label='Title')
    item = forms.ChoiceField(widget=forms.Select, required=False, label='If',
                             choices=items)
    action = forms.ChoiceField(widget=forms.Select, required=False, label='is',
                               choices=actions)
    word = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'a word'}))
