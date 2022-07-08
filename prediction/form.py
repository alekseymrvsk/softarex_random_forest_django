from django import forms
from .models import Files


class StudentForm(forms.Form):
    model = Files
    fields = ['file']
    file = forms.FileField()
