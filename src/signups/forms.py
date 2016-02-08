from django import forms

from .models import SignUp
from models import UploadFile

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = "__all__" 
    #code

class UploadFileForm(forms.ModelForm):
    
    class Meta:
        model = UploadFile
        fields = "__all__" 

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )      
