from email.policy import default
from django import forms
from django.forms.widgets import NumberInput
from accounts.models import Account
from support_request.models import SectorRegionList, ClientList, MyRequest


USER_CHOICES = [
    ('Systems Assurance', 'Systems Assurance'),
    ('Data Science', 'Data Science'),
]

class RequestForm(forms.ModelForm):

    directorate = forms.ModelChoiceField(
        queryset=SectorRegionList.objects.all(), empty_label="Select regional office or sector from list")

    client = forms.ModelChoiceField(
        queryset=ClientList.objects.all(), empty_label="Select client from list")

    assigned_officer = forms.ModelChoiceField(queryset=Account.objects.filter(on_assignment=False), empty_label="Select officer to assign this request")

    requested_date_from = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    requested_date_to = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    allocated_date_from = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    allocated_date_to = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = MyRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = '@oagkenya.go.ke'
        self.fields['request_category'].widget.attrs['placeholder'] = 'Request category'
        self.fields['other_client'].widget.attrs['placeholder'] = 'Enter the name of the client if not in above list'
        self.fields['requested_date_from'].widget.attrs['placeholder'] = 'Tentative date for beginning support'
        self.fields['requested_date_to'].widget.attrs['placeholder'] = 'Tentative date request will be completed'
        self.fields['allocated_date_from'].widget.attrs['placeholder'] = 'Date for beginning support'
        self.fields['allocated_date_to'].widget.attrs['placeholder'] = 'Date request will be completed'
        self.fields['phone_number'].widget.attrs['placeholder'] = '07xxxxxxxx'
        self.fields['directorate'].widget.attrs['placeholder'] = 'Select regional office or sector from list'
        self.fields['client'].widget.attrs['placeholder'] = 'Select client from list'
        self.fields['assigned_officer'].widget.attrs['placeholder'] = 'Select officer to assign this request'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
