from django import forms
from django.forms.extras.widgets import SelectDateWidget


# Add a simple form for opportunity creating new rss sources, that must to be parsed.
class AddRssSource(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    link = forms.CharField(max_length=500, required=True)


BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)

class CommentForm(forms.Form):
    birth_year = forms.DateField(widget=SelectDateWidget())
    favorite_colors = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)
