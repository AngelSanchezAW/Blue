from django import forms
from analis.models import SitioWeb

class SitioWebChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre
    
class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Fecha de inicio', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Fecha de fin', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    sitios_web = SitioWebChoiceField(queryset=SitioWeb.objects.all(), required=False, label='Sitios web')