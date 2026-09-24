import re

from django import forms

from .models import ZuluWord

# Letters (incl. isiZulu/English), digits, spaces and common punctuation only.
SAFE_TEXT = re.compile(r"^[\w\s'’\-.,?!]+$", re.UNICODE)

SEARCH_TYPES = [
    ('word', 'Word / translation'),
    ('phrase', 'Phrases & example sentences'),
    ('definition', 'Cultural context'),
]


class SearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        max_length=100,
        strip=True,
        error_messages={
            'required': 'Please enter a valid word.',
            'max_length': 'Search text is too long (maximum 100 characters).',
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter isiZulu, English, or Swati word...',
            'class': 'search-input',
        }),
    )
    search_type = forms.ChoiceField(choices=SEARCH_TYPES, required=False, label='Search in')
    pos = forms.ChoiceField(
        choices=[('', 'All')] + ZuluWord.PARTS_OF_SPEECH,
        required=False,
        label='Part of speech',
    )
    exact_match = forms.BooleanField(required=False, label='Exact match')

    def clean_q(self):
        q = self.cleaned_data['q']
        if not SAFE_TEXT.match(q):
            raise forms.ValidationError('Please enter a valid word.')
        return q


class FavouriteSearchForm(forms.Form):
    """Search box on the Favourites panel."""
    q = forms.CharField(
        required=False,
        max_length=100,
        strip=True,
        label='Search favourites',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search your favourites...',
            'class': 'search-input',
        }),
    )

    def clean_q(self):
        q = self.cleaned_data['q']
        if q and not SAFE_TEXT.match(q):
            raise forms.ValidationError('Please enter a valid search term.')
        return q
