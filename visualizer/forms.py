# visualizer/forms.py

from django import forms
from .widgets import CustomFileInput

class RouteFileForm(forms.Form):
    csv_files = forms.FileField(widget=CustomFileInput(attrs={'multiple': True}))
