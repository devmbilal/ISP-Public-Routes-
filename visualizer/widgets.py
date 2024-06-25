# visualizer/widgets.py

from django.forms.widgets import ClearableFileInput

class CustomFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True

    def value_from_datadict(self, data, files, name):
        if isinstance(files.get(name), list):
            return files.getlist(name)
        return files.get(name)
