from django import forms
from django.forms.widgets import NumberInput
from .models import SectorRegionList, ClientList, MyRequest


USER_CHOICES = [
    ('Systems Assurance', 'Systems Assurance'),
    ('Data Science', 'Data Science'),
]

class RequestForm(forms.ModelForm):

    directorate = forms.ModelChoiceField(
        queryset=SectorRegionList.objects.all(), empty_label="Select regional office or sector from list")

    client = forms.ModelChoiceField(
        queryset=ClientList.objects.all(), empty_label="Select client from list")

    requested_date_from = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    requested_date_to = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MyRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = ClientList.objects.none()
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = '@oagkenya.go.ke'
        self.fields['request_category'].widget.attrs['placeholder'] = 'Request category'
        self.fields['other_client'].widget.attrs['placeholder'] = 'Enter the name of the client if not in above list'
        self.fields['requested_date_from'].widget.attrs['placeholder'] = 'Tentative date for beginning support'
        self.fields['requested_date_to'].widget.attrs['placeholder'] = 'Tentative date request will be completed'
        self.fields['phone_number'].widget.attrs['placeholder'] = '07xxxxxxxx'
        self.fields['directorate'].widget.attrs['placeholder'] = 'Select regional office or sector from list'
        self.fields['client'].widget.attrs['placeholder'] = 'Select client from list'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


        if 'directorate' in self.data:
            try:
                directorate_id = int(self.data.get('directorate'))
                self.fields['client'].queryset = ClientList.objects.filter(regional_office__id=directorate_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['client'].queryset = self.instance.directorate.client_set.order_by('name')
