import re
from .util import list_entries

from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label="Entry", max_length=100)