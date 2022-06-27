import json
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import MyRequest, ClientList
from .forms import RequestForm
from django.contrib import messages, auth

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def new_request(request):
    form = RequestForm()
    if request.method == 'POST':
        directorate = request.POST['directorate']
        client = request.POST['client']
        form = RequestForm(request.POST)

        if form.is_valid():
            if MyRequest.objects.filter(directorate=directorate, client=client):
                messages.error(request, 'Request already exists!')
            else:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                directorate = form.cleaned_data['directorate']
                client = form.cleaned_data['client']
                email = form.cleaned_data['email']
                requested_date_from = form.cleaned_data['requested_date_from']
                requested_date_to = form.cleaned_data['requested_date_to']
                other_client = form.cleaned_data['other_client']
                support_request = MyRequest.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number, requested_date_from=requested_date_from,
                                                        requested_date_to=requested_date_to, other_client=other_client, directorate=directorate, client=client, email=email)
                support_request.phone_number = phone_number
                support_request.save()
                messages.success(request, 'Request submitted.')

                # SUPPORT REQUEST EMAIL
                current_site = get_current_site(request)
                mail_subject = 'New support request'
                message = render_to_string('requests/support_request_email.html', {
                    'support_request': support_request,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(support_request.pk)),

                })
                to_email = email
                bcc_email = 'samuel.kulola@oagkenya.go.ke'
                send_email = EmailMessage(mail_subject, message, to=[to_email], bcc=[bcc_email])
                send_email.send()
                return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RequestForm()
    context = {
        'form': form,
    }
    return render(request, 'requests/new_request.html', context)


def load_clients(request):
    data = json.loads(request.body)
    directorate_id = data['id']
    print(directorate_id)
    client = ClientList.objects.filter(regional_office__id=directorate_id)
    return JsonResponse(list(client.values("id", "name")), safe=False)
