
from django.shortcuts import render, redirect
from accounts.models import Account
from support_request.models import MyRequest
from .forms import RequestForm
from django.contrib.auth.decorators import login_required

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


@login_required(login_url='/support_request/new_request/')
def assign_request(request, id):
    assign_support_request = MyRequest.objects.get(pk=id)
    form = RequestForm(request.POST or None, instance=assign_support_request)
    context = {
        'assign_support_request': assign_support_request,
        'form': form,
    }

    if request.method == 'POST':
        if form.is_valid():
            request = MyRequest.objects.get(pk=id)
            assign_support_request.is_assigned = True
            form.save()
                                    # SUPPORT REQUEST EMAIL
            mail_subject = 'New support request'
            message = render_to_string('requests/support_assignment_email.html', {
                'assign_support_request': assign_support_request,
                'uid': urlsafe_base64_encode(force_bytes(assign_support_request.pk)),

            })
            to_email = request.assigned_officer
            bcc_email = 'samuel.kulola@oagkenya.go.ke'
            send_email = EmailMessage(mail_subject, message, to=[to_email], bcc=[bcc_email])
            send_email.send()

            return redirect ('dashboard')
    else:
        form = MyRequest()
    return  render(request, 'assign_request.html', context)


@login_required(login_url='/support_request/new_request/')
def dashboard(request):
    num_registered_users = Account.objects.all().count()    
    num_active_assignment = Account.objects.filter(on_assignment=True).count()
    num_available_officers = Account.objects.filter(on_assignment=False).count()
    num_requests_pending = MyRequest.objects.filter(is_assigned=False).count()
    num_requests_completed = MyRequest.objects.filter(is_assigned=True, is_completed=True).count()

    sa_ds_resources = Account.objects.all()
    requesting_officer = MyRequest.objects.all().filter(first_name='first_name')
    requesting_directorate = MyRequest.objects.all().filter(directorate__name='directorate')
    phone_number = MyRequest.objects.all().filter(phone_number='phone_number')
    client = MyRequest.objects.all().filter(client__name='client')
    
    context = {
        'num_registered_users': num_registered_users,
        'num_active_assignment': num_active_assignment,
        'num_available_officers': num_available_officers,
        'num_requests_pending': num_requests_pending,
        'num_requests_completed': num_requests_completed,

        'requesting_officer': requesting_officer,
        'requesting_directorate': requesting_directorate,
        'phone_number': phone_number,
        'client': client,
        'sa_ds_resources': sa_ds_resources,
        # 'date_from': date_from,
    }
    return render(request, 'dashboard.html', context=context)


@login_required(login_url='/support_request/new_request/')
def active_requests(request):
    active_support_requests = MyRequest.objects.filter(is_assigned=True)
    requesting_officer = MyRequest.objects.all().filter(first_name='first_name')
    requesting_directorate = MyRequest.objects.all().filter(directorate__name='directorate')
    phone_number = MyRequest.objects.all().filter(phone_number='phone_number')
    client = MyRequest.objects.all().filter(client__name='client')
    
    context = {
        'requesting_officer': requesting_officer,
        'requesting_directorate': requesting_directorate,
        'phone_number': phone_number,
        'client': client,
        'active_support_requests': active_support_requests,
        # 'date_from': date_from,
    }
    return render(request, 'active_requests.html', context=context)


@login_required(login_url='/support_request/new_request/')
def my_active_requests(request, assigned_officer_id):
    my_active_support_requests = MyRequest.objects.filter(assigned_officer_id=Account.id)
    requesting_officer = MyRequest.objects.all().filter(first_name='first_name')
    requesting_directorate = MyRequest.objects.all().filter(directorate__name='directorate')
    phone_number = MyRequest.objects.all().filter(phone_number='phone_number')
    client = MyRequest.objects.all().filter(client__name='client')
    
    context = {
        'requesting_officer': requesting_officer,
        'assigned_officer_id': assigned_officer_id,
        'requesting_directorate': requesting_directorate,
        'phone_number': phone_number,
        'client': client,
        'my_active_support_requests': my_active_support_requests,
    }
    return render(request, 'accounts/my_active_requests.html', context=context)


@login_required(login_url='/support_request/new_request/')
def pending_requests(request):
    pending_support_requests = MyRequest.objects.filter(is_assigned=False)
    requesting_officer = MyRequest.objects.all().filter(first_name='first_name')
    requesting_directorate = MyRequest.objects.all().filter(directorate__name='directorate')
    phone_number = MyRequest.objects.all().filter(phone_number='phone_number')
    client = MyRequest.objects.all().filter(client__name='client')
    
    context = {
        'requesting_officer': requesting_officer,
        'requesting_directorate': requesting_directorate,
        'phone_number': phone_number,
        'client': client,
        'pending_support_requests': pending_support_requests,
    }
    return render(request, 'pending_requests.html', context=context)


@login_required(login_url='/support_request/new_request/')
def completed_requests(request):
    completed_support_requests = MyRequest.objects.filter(is_assigned=True, is_completed=True)
    requesting_officer = MyRequest.objects.all().filter(first_name='first_name')
    requesting_directorate = MyRequest.objects.all().filter(directorate__name='directorate')
    phone_number = MyRequest.objects.all().filter(phone_number='phone_number')
    client = MyRequest.objects.all().filter(client__name='client')
    
    context = {
        'requesting_officer': requesting_officer,
        'requesting_directorate': requesting_directorate,
        'phone_number': phone_number,
        'client': client,
        'completed_support_requests': completed_support_requests,
    }
    return render(request, 'completed_requests.html', context=context)


@login_required(login_url='/support_request/new_request/')
def available_resources(request):
    num_registered_users = Account.objects.all().count()    
    num_active_assignment = Account.objects.filter(on_assignment=True).count()
    num_available_officers = Account.objects.filter(on_assignment=False).count()
    num_requests_pending = MyRequest.objects.filter(is_assigned=False).count()

    sa_ds_resources = Account.objects.all().filter(on_assignment=False)
    requesting_officer = MyRequest.objects.all().filter(first_name='first_name')
    requesting_directorate = MyRequest.objects.all().filter(directorate__name='directorate')
    phone_number = MyRequest.objects.all().filter(phone_number='phone_number')
    client = MyRequest.objects.all().filter(client__name='client')
    
    context = {
        'num_registered_users': num_registered_users,
        'num_active_assignment': num_active_assignment,
        'num_available_officers': num_available_officers,
        'num_requests_pending': num_requests_pending,

        'requesting_officer': requesting_officer,
        'requesting_directorate': requesting_directorate,
        'phone_number': phone_number,
        'client': client,
        'sa_ds_resources': sa_ds_resources,
    }
    return render(request, 'available_resources.html', context=context)
