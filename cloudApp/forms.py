# forms.py
from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()
    folder = forms.ChoiceField(choices=[(f.id, f.name) for f in Folder.objects.all()])
