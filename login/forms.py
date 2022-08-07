from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'user_id',
            'user_name',
        )
        widgets = {
            'user_name': forms.TextInput
        }
