from django import forms
#from django.views.generic.edit import FormView
from .models import EntryModel, SearchModel


class SearchForm(forms.ModelForm):
    class Meta:
        model = SearchModel
        fields = "__all__"


class EntryForm(forms.ModelForm):
    class Meta:
        model = EntryModel
        fields = "__all__"

        labels = {
            "title": "",
            "content": ""
        }

        widgets ={
        'title': forms.TextInput(attrs={'placeholder': 'Enter your title here..'}),
        'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your title (in markdown format eg. #Python..) and content here..'})
        }
