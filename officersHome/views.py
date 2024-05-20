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
from .models import Statement
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



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
@csrf_exempt
def queue_statement(request):
    if request.method == 'POST':
        statement = request.POST.get('statement')
        radio_value = request.POST.get('default-radio')
        
        # Collect other form fields as needed
        # ...

        if 'statements' not in request.session:
            request.session['statements'] = []

        request.session['statements'].append({
            'statement': statement,
            'radio_value': radio_value,
            # Include other form fields
        })
        request.session.modified = True

        return JsonResponse({'status': 'success'})



@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="docket.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        statements = request.session.get('statements', [])
        y = 750

        for i, statement_data in enumerate(statements):
            p.drawString(100, y, f"Statement {i+1}: {statement_data['radio_value']}")
            y -= 15
            p.drawString(100, y, statement_data['statement'])
            y -= 30

        p.showPage()
        p.save()

        buffer.seek(0)
        response.write(buffer.getvalue())

        # Clear session after generating PDF
        request.session.pop('statements', None)

        return response