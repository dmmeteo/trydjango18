import django_couch
from django import forms

base = django_couch.db('db')


# Add a simple form for opportunity creating new rss sources, that must to be parsed.
class AddRssSource(forms.Form):
    def __init__(self, *args, **kwargs):
        self.doc = kwargs.pop('doc', None)
        super(AddRssSource, self).__init__(*args, **kwargs)

    title = forms.CharField(max_length=255)
    link = forms.CharField(max_length=500)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        view = base.view('subscriptions/source_exists', key=title).rows

        if self.doc:
            return title
        elif view:
            raise forms.ValidationError('This title already exists.')
        else:
            return title


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
        self.doc = kwargs.pop('doc', None)
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

    def clean_title(self):
        title = self.cleaned_data.get('title')
        view = base.view('subscriptions/filter_exists', key=title).rows

        if self.doc:
            return title
        elif view:
            raise forms.ValidationError('This title of filter already exists.')
        else:
            return title
