from django import forms
from .models import Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields= ['image']
        widgets = {'image': forms.FileInput(attrs={'class': 'form-control'})}