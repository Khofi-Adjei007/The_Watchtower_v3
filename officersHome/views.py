from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import datetime
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
import logging
from django.http import JsonResponse
logger = logging.getLogger(__name__)
from django.utils import timezone
from reportlab.lib.pagesizes import A4




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
    try:
        # Retrieve queued statements from session
        queued_statements = request.session.get('queued_statements', [])

        # Check if queued statements exist
        if isinstance(queued_statements, list) and queued_statements:
            # Format queued statements
            formatted_statements = {}
            for index, statement_content in enumerate(queued_statements):
                formatted_statements[str(index)] = statement_content

            # Return formatted statements as JSON response
            return JsonResponse(formatted_statements)
        else:
            # If no queued statements exist, return an empty dictionary as JSON response
            return JsonResponse({})
    except Exception as e:
        logger.exception("Error occurred while previewing the PDF")
        return JsonResponse({"error": str(e)}, status=500)




@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        # Retrieve queued statements from session
        queued_statements = request.session.get('queued_statements', [])

        # Check if queued statements exist
        if isinstance(queued_statements, list) and queued_statements:
            # Create a new PDF document with a padding of 2 inches around the entire page
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="docket.pdf"'

            # Create a ReportLab canvas with letter size and 2 inches padding
            pdf = canvas.Canvas(response, pagesize=(letter[0] - 144, letter[1] - 144))

            # Set initial position with padding
            x_position = 72  # 1 inch padding from left
            y_position = letter[1] - 72  # 1 inch padding from top

            # Iterate through queued statements and write them to the PDF
            for index, statement_content in enumerate(queued_statements):
                # Add a page break before writing new statement content
                if index > 0:
                    pdf.showPage()

                # Ensure statement_content is a string
                if isinstance(statement_content, dict):
                    # Convert dict to string
                    statement_content = str(statement_content)

                # Calculate the width of the text
                text_width = pdf.stringWidth(statement_content, "Helvetica", 12)

                # Check if the text exceeds the available width
                if x_position + text_width > letter[0] - 72:  # Check if text goes beyond right padding
                    # Move to the next line
                    y_position -= 20  # Assuming font size 12, adjust as needed
                    # Reset x_position to start from the left edge
                    x_position = 72

                # Check if the text goes beyond the bottom padding
                if y_position < 72:
                    # Add a new page
                    pdf.showPage()
                    # Reset y_position to the top edge with padding
                    y_position = letter[1] - 72

                # Write statement content to PDF
                pdf.drawString(x_position, y_position, statement_content)

                # Move to the next line
                y_position -= 20  # Assuming font size 12, adjust as needed

            # Save the PDF document
            pdf.save()

            # Return the PDF as response
            return response
        else:
            # If no queued statements exist, return an error response
            return JsonResponse({'success': False, 'error': 'Queue is empty'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@csrf_exempt
def save_pdf(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            pdf_file = request.FILES['file']

            # Generate a unique filename
            officer_current_station = request.user.newofficerregistration.officer_current_station
            current_user = request.user.username
            current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{officer_current_station}_{current_user}_{current_datetime}_docket.pdf"

            # Define the file path
            file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)

            # Create directory if it does not exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the file
            with open(file_path, 'wb') as f:
                for chunk in pdf_file.chunks():
                    f.write(chunk)

            # Save file info to the database
            #PDFDocument.objects.create(user=request.user, file_path=file_path)

            # Clear the session queue
            request.session['queued_statements'] = []

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No file found in the request'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)