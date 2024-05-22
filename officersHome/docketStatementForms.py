from django import forms
from .models import Statements


class CaseStatementForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = ['name', 'residential_address', 'contact', 'date_of_birth', 'hometown', 'gender', 'occurrence']
        widgets = {'statement_type': forms.HiddenInput()}


class VictimStatementForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = ['name', 'residential_address', 'contact', 'date_of_birth', 'hometown', 'gender', 'occurrence']
        widgets = {'statement_type': forms.HiddenInput()}


class SuspectStatementForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = ['name', 'residential_address', 'contact', 'date_of_birth', 'hometown', 'gender', 'occurrence']
        widgets = {'statement_type': forms.HiddenInput()}
