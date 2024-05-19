from django import forms
from .models import Statements


class StatementForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = ['category', 'name', 'address', 'contact', 'date_of_birth', 'hometown', 'gender', 'content']
        widgets = {
            'category': forms.RadioSelect,
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 8}),
        }