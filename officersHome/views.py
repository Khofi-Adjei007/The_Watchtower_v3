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
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from .models import Statement, PDFDocument






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

def profile_view(request):
    context = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'newofficerregistration'):
            context['officer_profile_image_url'] = request.user.newofficerregistration.officer_profile_image.url if request.user.newofficerregistration.officer_profile_image else None
    return render(request, 'profile.html', context)



###################################################################################
@csrf_exempt
def queue_statement(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Store data in session
        request.session['queued_statements'] = request.session.get('queued_statements', [])
        request.session['queued_statements'].append(data)
        request.session.modified = True
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)



@csrf_exempt
def check_session(request):
    # Check if session data exists
    session_populated = 'queued_statements' in request.session and bool(request.session['queued_statements'])

    # Return a JSON response indicating the session state
    return JsonResponse({'session_populated': session_populated})


@csrf_exempt
def clear_session(request):
    if request.method == 'POST':
        # Clear specific session data
        if 'queued_statements' in request.session:
            del request.session['queued_statements']
        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@csrf_exempt
def preview_pdf(request):
    # Retrieve queued statements from session
    queued_statements = request.session.get('queued_statements', [])

    # Check if queued statements exist
    if isinstance(queued_statements, list) and queued_statements:
        # Format queued statements
        formatted_statements = {}
        for index, statement_content in enumerate(queued_statements):
            formatted_statements[str(index)] = {
                'content': statement_content
            }

        # Return formatted statements as JSON response
        return JsonResponse(formatted_statements)
    else:
        # If no queued statements exist, return an empty dictionary as JSON response
        return JsonResponse({})



@csrf_exempt
def generate_pdf(request):
    print("generate_pdf view called")  # Debugging statement
    session_key = request.session.session_key
    if not session_key:
        return HttpResponse("No statements queued", status=400)
    
    session = Session.objects.get(session_key=session_key)
    statements = Statement.objects.filter(session=session)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.drawString(100, 800, "Docket Report")
    
    y = 750
    for statement in statements:
        p.drawString(100, y, f"{statement.statement_type} - {statement.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 15
        text = p.beginText(100, y)
        text.textLines(statement.content)
        p.drawText(text)
        y -= len(statement.content.split('\n')) * 15 + 20
    
    p.showPage()
    p.save()

    buffer.seek(0)
    pdf_content = buffer.getvalue()

    pdf_document = PDFDocument()
    pdf_document.file.save('docket.pdf', ContentFile(pdf_content))

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="docket.pdf"'
    
    Statement.objects.filter(session=session).delete()
    return response
