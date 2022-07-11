from django import forms
from .models import Files
from django.forms import FileInput


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file',)
        widgets = {'file': FileInput()}
