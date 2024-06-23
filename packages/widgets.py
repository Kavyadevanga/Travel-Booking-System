# packages/widgets.py

from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return super().value_from_datadict(data, files, name)
