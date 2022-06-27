from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from accounts.models import Account


class SectorRegionList(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'directorate'
        verbose_name_plural = 'directorates'

    def __str__(self):
        return self.name


class ClientList(models.Model):
    regional_office = models.ForeignKey(
        SectorRegionList, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Check that dates are not in the past
def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")


class MyRequest(models.Model):

    USER_CHOICES = [
    ('Systems Assurance', 'Systems Assurance'),
    ('Data Science', 'Data Science'),]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    directorate = models.ForeignKey(SectorRegionList, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(ClientList, on_delete=models.SET_NULL, null=True)
    other_client = models.CharField(max_length=30, default=None)
    request_category = models.CharField(max_length=30, choices=USER_CHOICES, default="Systems Assurance")
    requested_date_from = models.DateField(validators=[validate_date])
    requested_date_to = models.DateField(validators=[validate_date])
    date_request_submitted = models.DateTimeField(auto_now_add=True)
    date_request_assigned = models.DateTimeField(auto_now=True)
    is_assigned = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    allocated_date_from = models.DateField(null=True, blank=True)
    allocated_date_to = models.DateField(null=True, blank=True)
    assigned_officer = models.ForeignKey(Account, blank=True, null=True, on_delete=models.DO_NOTHING)
    last_login =  models.DateTimeField(auto_now_add=True, blank=True)

    def create_request(self, first_name, last_name, email, phone_number, request_category, directorate, client, other_client,
                       requested_date_from, assigned_officer, requested_date_to, date_request_submitted=date_request_submitted):
        request = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            directorate=directorate,
            assigned_officer=assigned_officer,
            client=client,
            other_client=other_client,
            request_category=request_category,
            requested_date_from=requested_date_from,
            requested_date_to=requested_date_to,
            date_request_submitted=date_request_submitted,
        )
        request.save(using=self._db)

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@oagkenya.go.ke" not in data:   # any check you need
            raise ValueError("Please use your OAG email address")
        return data

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.request_category


# Check if requested end date of request is not before start date
def check_date(sender, instance, *args, **kwargs):
    if instance.requested_date_from > instance.requested_date_to:
        raise ValidationError('Date to cannot be before date from')
    

pre_save.connect(check_date, sender=MyRequest)

