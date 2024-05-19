from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import NewOfficerRegistration,OfficerLogin
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from .officerRegistrationsForms import officerRegistrationsForms, officer_loginForms
from django.contrib.auth.hashers import make_password, check_password
import json
from io import BytesIO
from django.shortcuts import render, redirect
from .docketStatementForms import StatementForm
from .models import Statements, Docket
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings
import os





# officer Registrations Views
def redirect_with_delay(request, url, delay_seconds=3):
    return render(request, 'redirect_with_delay.html', {'url': url, 'delay_seconds': delay_seconds})


# Home page view
@login_required
def HomePage(request):
    return render(request, 'HomePage.html')


# New Officers Registration Views
@csrf_protect
def officer_registrations(request):
    if request.method == "POST":
        form = officerRegistrationsForms(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            user, created = User.objects.get_or_create(username=form_data['username'], email=form_data['email'])
            if created:
                user.set_password(form_data['password'])
                user.save()

            NewOfficerRegistration.objects.create(
                user=user,
                first_name=form_data['first_name'],
                middle_name=form_data['middle_name'],
                last_name=form_data['last_name'],
                username=form_data['username'],
                officer_gender=form_data['officer_gender'],
                email=form_data['email'],
                phone_contact=form_data['phone_contact'],
                officer_address=form_data['officer_address'],
                officer_staff_ID=form_data['officer_staff_ID'],
                officer_qualification=form_data['officer_qualification'],
                officer_date_of_birth=form_data['officer_date_of_birth'],
                officer_operations_region=form_data['officer_operations_region'],
                officer_current_rank=form_data['officer_current_rank'],
                officer_current_station=form_data['officer_current_station'],
                officer_operations_department=form_data['officer_operations_department'],
                officer_profile_image=form_data['officer_profile_image'],
                officer_stationRank=form_data['officer_stationRank'],
            )

            messages.success(request, 'Registration successful!')
            return redirect_with_delay(request, reverse('officer_login'), delay_seconds=2)
    else:
        form = officerRegistrationsForms()
    return render(request, 'officer_registrations.html', {"form": form})



# officer login views
@csrf_protect
def officer_login(request):
    error_message = ''
    if request.method == 'POST':
        form = officer_loginForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                if hasattr(user, 'newofficerregistration'):
                    request.session['officer_staff_ID'] = user.newofficerregistration.officer_staff_ID
                    request.session['officer_current_rank'] = user.newofficerregistration.officer_current_rank
                return redirect('HomePage')
            else:
                error_message = 'Invalid username or password'
        else:
            error_message = 'Invalid form data'
    else:
        form = officer_loginForms()
    return render(request, 'officer_login.html', {'form': form, 'error_message': error_message})




# officer logout views
def officer_logout(request):
    logout(request)
    request.session.flush()  # This ensures the session is completely cleared
    return redirect(reverse('officer_login'))

# full Casebox details
def full_casebox_details(request):
    return render(request, 'Casebox.html')




###################################################################################
#Docket Process Views Starts Here
def index(request):
    if request.method == 'POST':
        form = StatementForm(request.POST)
        if form.is_valid():
            statement = form.save()
            # Handle statement queuing logic (store in session or similar)
            queued_statements = request.session.get('queued_statements', [])
            queued_statements.append(statement.id)
            request.session['queued_statements'] = queued_statements
            form = StatementForm()  # Reset the form for the next input
    else:
        form = StatementForm()
    return render(request, 'HomePage.html', {'form': form})


def register_docket(request):
    queued_statements = request.session.get('queued_statements', [])
    if queued_statements:
        statements = Statements.objects.filter(id__in=queued_statements)
        docket = Docket.objects.create()
        docket.statements.set(statements)
        docket.save()
        request.session['queued_statements'] = []  # Clear the session queue
    return redirect(reverse('HomePage'))

