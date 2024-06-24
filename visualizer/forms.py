from django import forms
from .models import RouteFile

class RouteFileForm(forms.ModelForm):
    class Meta:
        model = RouteFile
        fields = ['csv_file']
