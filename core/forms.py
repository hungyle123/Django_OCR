from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields= ['image']
        widgets = {'image': forms.FileInput(attrs={'class': 'form-control'})}