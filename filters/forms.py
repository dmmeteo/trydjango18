from django import forms

# Define our choices for filter's form
items = (
    ('item1', 'Title'),
    ('item2', 'Description')
)

actions = (
    ('action1', 'Contains'),
    ('action2', 'Does not contain')
)


# FiltersForm is print out two select elements and an one required textinput's field
class FiltersForm(forms.Form):
    item = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker'}), required=False, label='If',
                             choices=items)
    action = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectpicker'}), required=False, label='is',
                               choices=actions)
    word = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'a word'}), required=True)
