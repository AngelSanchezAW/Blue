from django import forms

class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Fecha de inicio', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Fecha de fin', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
