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
from .docketvalidationForms import CaseStep1Form, CaseStep2Form, CaseStep3Form
from .models import Case
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import NewOfficerRegistration


# Home Selector
@csrf_exempt
def selectPurpose(request):
    return render(request, 'selectPurpose.html')

# Route to Search Database
def searchdatabase(request):
    return render(request, 'searchdatabase.html')

# Route to get cases and thier progress
def casesProgress(request):
    return render(request, 'casesProgress.html')

# Route to command messaging
def commandmessaging(request):
    return render(request, 'commandmessaging.html')


    
def docketforms(request):
    # Initialize forms for all steps
    form_step1 = CaseStep1Form()
    form_step2 = CaseStep2Form()
    form_step3 = CaseStep3Form()

    if request.method == 'POST':
        # Process form submission for step 1
        form_step1 = CaseStep1Form(request.POST)
        if form_step1.is_valid():
            # Handle the valid form, e.g., save data or redirect
            return redirect('next_step_view')  # Adjust the URL as needed
        # If the form is not valid, it will fall through to render with errors
        # Keep form_step2 and form_step3 as initialized above

    # Render the forms in the template
    return render(request, 'docketforms.html', {
        'form_step1': form_step1,
        'form_step2': form_step2,
        'form_step3': form_step3,
    })

def CaseStep1View(request):
    if request.method == 'POST':
        form = CaseStep1Form(request.POST)  # Instantiate the form with POST data
        if form.is_valid():
            # Store form data in session
            request.session['case_title'] = form.cleaned_data.get('case_title')
            request.session['date_time_of_incident'] = form.cleaned_data.get('date_time_of_incident')
            request.session['date_time_of_report'] = form.cleaned_data.get('date_time_of_report')

            # Complainant Information
            request.session['complainant_name'] = form.cleaned_data.get('complainant_name')
            request.session['complainant_contact'] = form.cleaned_data.get('complainant_contact')
            request.session['complainant_physical_address'] = form.cleaned_data.get('complainant_physical_address')
            request.session['complainant_digital_address'] = form.cleaned_data.get('complainant_digital_address')
            request.session['complainant_occupation'] = form.cleaned_data.get('complainant_occupation')
            request.session['complainant_date_of_birth'] = form.cleaned_data.get('complainant_date_of_birth')

            # Suspect Information
            request.session['suspect_name'] = form.cleaned_data.get('suspect_name')
            request.session['suspect_contact'] = form.cleaned_data.get('suspect_contact')
            request.session['suspect_physical_address'] = form.cleaned_data.get('suspect_physical_address')
            request.session['suspect_digital_address'] = form.cleaned_data.get('suspect_digital_address')
            request.session['suspect_occupation'] = form.cleaned_data.get('suspect_occupation')
            request.session['suspect_date_of_birth'] = form.cleaned_data.get('suspect_date_of_birth')

            # Victim Information
            request.session['is_victim_same_as_complainant'] = form.cleaned_data.get('is_victim_same_as_complainant')
            request.session['victim_name'] = form.cleaned_data.get('victim_name')
            request.session['victim_contact'] = form.cleaned_data.get('victim_contact')
            request.session['victim_physical_address'] = form.cleaned_data.get('victim_physical_address')
            request.session['victim_digital_address'] = form.cleaned_data.get('victim_digital_address')
            request.session['victim_occupation'] = form.cleaned_data.get('victim_occupation')
            request.session['victim_date_of_birth'] = form.cleaned_data.get('victim_date_of_birth')

            # Incident Details
            request.session['location_of_incident'] = form.cleaned_data.get('location_of_incident')
            request.session['type_of_incident'] = form.cleaned_data.get('type_of_incident')
            request.session['statement_of_incident'] = form.cleaned_data.get('statement_of_incident')

            # Key Witness Information
            request.session['key_witness_name'] = form.cleaned_data.get('key_witness_name')
            request.session['key_witness_contact'] = form.cleaned_data.get('key_witness_contact')
            request.session['key_witness_physical_address'] = form.cleaned_data.get('key_witness_physical_address')
            request.session['key_witness_digital_address'] = form.cleaned_data.get('key_witness_digital_address')

            # Proceed to the next step or save the data
            return redirect('CaseStep2Form')  # Replace 'step2' with the name of the URL pattern for the next step
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CaseStep1Form()  # Instantiate an empty form
    return render(request, 'docketforms.html', {'form': form})

def CaseStep2View(request):
    if request.method == 'POST':
        form = CaseStep2Form(request.POST)
        if form.is_valid():
            # Store form data in session
            request.session['complainant_statement'] = form.cleaned_data.get('complainant_statement')
            request.session['suspect_statement'] = form.cleaned_data.get('suspect_statement')
            request.session['witness_statement'] = form.cleaned_data.get('witness_statement')
            request.session['additional_witnesses'] = form.cleaned_data.get('additional_witnesses')

            # Proceed to the next step or save the data
            return redirect('CaseStep3Form')  # Replace 'step3' with the name of the URL pattern for the next step
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CaseStep2Form()  # Instantiate an empty form
    
    return render(request, 'docketforms.html', {'form': form})

def CaseStep3View(request):
    if request.method == 'POST':
        form = CaseStep3Form(request.POST, request.FILES)  # Handle both POST data and uploaded files
        if form.is_valid():
            # Retrieve data from the session
            case_data = {
                'case_title': request.session.get('case_title'),
                'date_time_of_incident': request.session.get('date_time_of_incident'),
                'date_time_of_report': request.session.get('date_time_of_report'),

                # Complainant Information
                'complainant_name': request.session.get('complainant_name'),
                'complainant_contact': request.session.get('complainant_contact'),
                'complainant_physical_address': request.session.get('complainant_physical_address'),
                'complainant_digital_address': request.session.get('complainant_digital_address'),
                'complainant_occupation': request.session.get('complainant_occupation'),
                'complainant_date_of_birth': request.session.get('complainant_date_of_birth'),

                # Suspect Information
                'suspect_name': request.session.get('suspect_name'),
                'suspect_contact': request.session.get('suspect_contact'),
                'suspect_physical_address': request.session.get('suspect_physical_address'),
                'suspect_digital_address': request.session.get('suspect_digital_address'),
                'suspect_occupation': request.session.get('suspect_occupation'),
                'suspect_date_of_birth': request.session.get('suspect_date_of_birth'),

                # Victim Information
                'is_victim_same_as_complainant': request.session.get('is_victim_same_as_complainant'),
                'victim_name': request.session.get('victim_name'),
                'victim_contact': request.session.get('victim_contact'),
                'victim_physical_address': request.session.get('victim_physical_address'),
                'victim_digital_address': request.session.get('victim_digital_address'),
                'victim_occupation': request.session.get('victim_occupation'),
                'victim_date_of_birth': request.session.get('victim_date_of_birth'),

                # Incident Details
                'location_of_incident': request.session.get('location_of_incident'),
                'type_of_incident': request.session.get('type_of_incident'),
                'statement_of_incident': request.session.get('statement_of_incident'),

                # Key Witness Information
                'key_witness_name': request.session.get('key_witness_name'),
                'key_witness_contact': request.session.get('key_witness_contact'),
                'key_witness_physical_address': request.session.get('key_witness_physical_address'),
                'key_witness_digital_address': request.session.get('key_witness_digital_address'),

                # Final step data from the current form submission
                'reporting_officer_name': form.cleaned_data.get('reporting_officer_name'),
                'reporting_officer_badge_id': form.cleaned_data.get('reporting_officer_badge_id'),
                'reporting_officer_rank': form.cleaned_data.get('reporting_officer_rank'),
                'reporting_officer_station': form.cleaned_data.get('reporting_officer_station'),
                'reporting_officer_division': form.cleaned_data.get('reporting_officer_division'),
                'charges_filed': form.cleaned_data.get('charges_filed'),
                'legal_actions_taken': form.cleaned_data.get('legal_actions_taken'),
                'assigned_investigator': form.cleaned_data.get('assigned_investigator'),
                'case_status': form.cleaned_data.get('case_status'),
                'follow_up_required': form.cleaned_data.get('follow_up_required'),
                'additional_notes': form.cleaned_data.get('additional_notes'),
            }

            # Handle file uploads separately and add to case_data
            mugshot = form.cleaned_data.get('mugshot')
            fingerprint = form.cleaned_data.get('fingerprint')

            # Create the Docket instance with all the collected data
            docket = docketforms.objects.create(**case_data)

            # Save the files if they exist
            if mugshot:
                docket.mugshot = mugshot
            if fingerprint:
                docket.fingerprint = fingerprint
            docket.save()

            # Clear the session after saving
            request.session.flush()

            messages.success(request, "Docket successfully registered.")
            return redirect('success_page')  # Replace with the name of your success URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CaseStep3Form()  # Instantiate an empty form for GET requests

    return render(request, 'docketforms.html', {'form': form})




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


# badge Verification view
@csrf_exempt
@require_POST
def verify_badge(request):
    badge_number = request.POST.get('officer_staff_ID')
    if NewOfficerRegistration.objects.filter(officer_staff_ID=badge_number).exists():
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid badge number'})





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
                return redirect('selectPurpose')
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
    request.session.flush()
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