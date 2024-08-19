from django import forms
from .models import Case
from datetime import datetime
import uuid
import re
from django.core.exceptions import ValidationError




class CaseStep1Form(forms.Form):
    case_ID = forms.CharField(label="Case ID", max_length=100, required=False, widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Auto-generated',
            'disabled': 'disabled'
        }))

    def __init__(self, *args, **kwargs):
        super(CaseStep1Form, self).__init__(*args, **kwargs)
        # Generate a unique ID if this is a new form instance
        if 'initial' in kwargs:
            self.fields['case_ID'].initial = kwargs['initial'].get('case_ID', str(uuid.uuid4()))
        else:
            self.fields['case_ID'].initial = str(uuid.uuid4())

    def clean_case_ID(self):
        case_ID = self.cleaned_data.get('case_ID')
        if not case_ID:
            raise ValidationError("Case ID cannot be empty.")
        # Assuming NewDocket is your model where case_IDs are stored
        if CaseStep1Form.objects.filter(case_ID=case_ID).exists():
            raise ValidationError("Case ID already exists. Please reload the form.")
        return case_ID

    def save(self, data):
        new_docket = CaseStep1Form(case_ID=self.cleaned_data['case_ID'],)
        new_docket.save()
        return new_docket


    Case_Title = forms.CharField(required=False,max_length=250,)
    def clean_Case_Title(self):
        Case_Title = self.cleaned_data.get('clean_Case_Title')
        if Case_Title and not re.match(r'^[a-zA-Z]*$', Case_Title):
            raise forms.ValidationError(("Enter a Case_Title"))
        return Case_Title


    #Incident Time Stamp
    date_time_of_incident = forms.DateTimeField(
        label="Date & Time Of Incident",
        error_messages={'required': 'Indicate Time and Date'},
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
    )

    def clean_date_time_of_incident(self):
        date_time_of_incident = self.cleaned_data.get('date_time_of_incident')
        # Validation: Ensure the date is in the correct format or any other checks you need
        # Example: Ensure the datetime is not in the future
        if date_time_of_incident:
            # Add your custom validation logic if needed
            pass
        return date_time_of_incident


    #Report Time Stamp
    date_time_of_report = forms.DateTimeField(label="Date & Time of Report", required=True, 
                                              widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                              error_messages={'required': 'Indicate Time and Date'})
    def clean_date_time_of_report(self):
        date_time_of_report = self.cleaned_data.get('date_time_of_report')
        if not date_time_of_report:
            raise ValidationError("Date & Time of Report is required.")
        # Ensure the date is not in the future
        from datetime import datetime
        if date_time_of_report > datetime.now():
            raise ValidationError("The report date cannot be in the future.")
        return date_time_of_report
    
    #Complainant Name Stamp
    complainant_name = forms.CharField(label="Enter complainant_name", max_length=100,
                                 error_messages={'required': 'complainant name is Required',
                                                    'invalid': 'Name is Invalid.'})
    def clean_complainant_name(self):
        complainant_name = self.cleaned_data.get('complainant_name')
        if not complainant_name:
            raise forms.ValidationError(("First name cannot be empty."))
        elif not re.match(r'^[a-zA-Z]*$', complainant_name):
            raise forms.ValidationError(("Enter a valid first name."))
        return complainant_name


    complainant_contact = forms.CharField(label="complainant Contact", max_length=15,required=True,
                                          widget=forms.TextInput(attrs={'placeholder': 'e.g., +1234567890'}),
                                          error_messages={'required': 'Phone number is required.'})
    def clean_complainant_contact(self):
        complainant_contact = self.cleaned_data.get('complainant_contact')
        phone_pattern = re.compile(r'^\+?\d{7,15}$')
        if not phone_pattern.match(complainant_contact):
            raise ValidationError("Enter a valid phone number with 7 to 15 digits.")
        return complainant_contact
    

    complainant_physical_address = forms.CharField(label="complainant_physical_address", max_length=100,
                                 error_messages={'required': 'complainant_physical_address is Required',
                                                    'invalid': 'complainant_physical_address is Invalid.'})
    def clean_complainant_physical_address(self):
        complainant_physical_address = self.cleaned_data.get('complainant_physical_address')
        if not complainant_physical_address:
            raise forms.ValidationError(("complainant_physical_address cannot be empty."))
        elif not re.match(r'^[a-zA-Z]*$', complainant_physical_address):
            raise forms.ValidationError(("Enter a valid address."))
        return complainant_physical_address
    

    complainant_digital_address = forms.CharField(label="complainant_digital_address", max_length=100,
                                                  error_messages={'required': 'complainant_digital_address is Required',
                                                                  'invalid': 'complainant_digital_address is Invalid.'})
    def clean_complainant_digital_address(self):
        complainant_digital_address = self.cleaned_data.get('complainant_digital_address')
        if not complainant_digital_address:
            raise forms.ValidationError(("complainant_digital_address cannot be empty"))
        elif not re.match(r'^[a-zA-Z]*$', complainant_digital_address):
            raise forms.ValidationError(("Enter a valid address"))
        return complainant_digital_address
    
    
    complainant_occupation = forms.CharField(label="complainant_digital_address", max_length=100,
                                                  error_messages={'required': 'complainant_digital_address is Required',
                                                                  'invalid': 'complainant_digital_address is Invalid.'})
    def clean_complainant_occupation(self):
        complainant_occupation = self.cleaned_data.get('complainant_occupation')
        if not complainant_occupation:
            raise forms.ValidationError(("complainant_digital_address cannot be empty"))
        elif not re.match(r'^[a-zA-Z]*$', complainant_occupation):
            raise forms.ValidationError(("Enter a valid address"))
        return complainant_occupation
    

    complainant_date_of_birth = forms.DateField(label="Complainant Date of Birth", required=True,
                                            widget=forms.DateInput(attrs={'type': 'date'}),
                                            error_messages={'required': 'Date of birth is required.'})

    def clean_complainant_date_of_birth(self):
        complainant_date_of_birth = self.cleaned_data.get('complainant_date_of_birth')
        if not complainant_date_of_birth:
            raise forms.ValidationError("Date of birth cannot be empty.")
        return complainant_date_of_birth

        
    suspect_name = forms.CharField(label="Suspect Name", max_length=100,
                               error_messages={'required': 'Suspect name is required.'})
    def clean_suspect_name(self):
        suspect_name = self.cleaned_data.get('suspect_name')
        if not suspect_name:
            raise forms.ValidationError("Suspect name cannot be empty.")
        elif not re.match(r'^[a-zA-Z ]*$', suspect_name):  # Allow spaces in names
            raise forms.ValidationError("Enter a valid name (letters and spaces only).")
        return suspect_name


    suspect_contact = forms.CharField(label="Suspect Contact", max_length=15, required=True,
                                      widget=forms.TextInput(attrs={'placeholder': 'e.g., +1234567890'}),
                                      error_messages={'required': 'Phone number is required.'})
    def clean_suspect_contact(self):
        suspect_contact = self.cleaned_data.get('suspect_contact')
        phone_pattern = re.compile(r'^\+?\d{7,15}$')
        if not phone_pattern.match(suspect_contact):
            raise forms.ValidationError("Enter a valid phone number with 7 to 15 digits.")
        return suspect_contact

    suspect_physical_address = forms.CharField(label="Suspect Physical Address", max_length=250,
                                           error_messages={'required': 'Physical address is required.'})
    def clean_suspect_physical_address(self):
        suspect_physical_address = self.cleaned_data.get('suspect_physical_address')
        if not suspect_physical_address:
            raise forms.ValidationError("Physical address cannot be empty.")
        return suspect_physical_address


    suspect_digital_address = forms.CharField(label="Suspect Digital Address", max_length=100,
                                          error_messages={'required': 'Digital address is required.'})
    def clean_suspect_digital_address(self):
        suspect_digital_address = self.cleaned_data.get('suspect_digital_address')
        if not suspect_digital_address:
            raise forms.ValidationError("Digital address cannot be empty.")
        return suspect_digital_address

    
    suspect_occupation = forms.CharField(label="Suspect Occupation", max_length=100,
                                     error_messages={'required': 'Occupation is required.'})
    def clean_suspect_occupation(self):
        suspect_occupation = self.cleaned_data.get('suspect_occupation')
        if not suspect_occupation:
            raise forms.ValidationError("Occupation cannot be empty.")
        elif not re.match(r'^[a-zA-Z ]*$', suspect_occupation):  # Allow spaces in occupations
            raise forms.ValidationError("Enter a valid occupation (letters and spaces only).")
        return suspect_occupation

    suspect_date_of_birth = forms.DateField(label="Suspect Date of Birth", required=True,
                                            widget=forms.DateInput(attrs={'type': 'date'}),
                                            error_messages={'required': 'Date of birth is required.'})
    def clean_suspect_date_of_birth(self):
        suspect_date_of_birth = self.cleaned_data.get('suspect_date_of_birth')
        if not suspect_date_of_birth:
            raise forms.ValidationError("Date of birth cannot be empty.")
        return suspect_date_of_birth

    is_victim_same_as_complainant = forms.BooleanField(label="Is Victim Same as Complainant?", required=False)

    def clean_is_victim_same_as_complainant(self):
        is_victim_same_as_complainant = self.cleaned_data.get('is_victim_same_as_complainant')
        return is_victim_same_as_complainant

    
    victim_name = forms.CharField(label="Victim Name", max_length=100,
                              error_messages={'required': 'Victim name is required.'})
    def clean_victim_name(self):
        victim_name = self.cleaned_data.get('victim_name')
        if not victim_name:
            raise forms.ValidationError("Victim name cannot be empty.")
        elif not re.match(r'^[a-zA-Z ]*$', victim_name):  # Allow spaces in names
            raise forms.ValidationError("Enter a valid name (letters and spaces only).")
        return victim_name


    victim_contact = forms.CharField(label="Victim Contact", max_length=15, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'e.g., +1234567890'}),
                                 error_messages={'required': 'Phone number is required.'})
    def clean_victim_contact(self):
        victim_contact = self.cleaned_data.get('victim_contact')
        phone_pattern = re.compile(r'^\+?\d{7,15}$')
        if not phone_pattern.match(victim_contact):
            raise forms.ValidationError("Enter a valid phone number with 7 to 15 digits.")
        return victim_contact


    victim_physical_address = forms.CharField(label="Victim Physical Address", max_length=250,
                                          error_messages={'required': 'Physical address is required.'})
    def clean_victim_physical_address(self):
        victim_physical_address = self.cleaned_data.get('victim_physical_address')
        if not victim_physical_address:
            raise forms.ValidationError("Physical address cannot be empty.")
        return victim_physical_address


    victim_digital_address = forms.CharField(label="Victim Digital Address", max_length=100,
                                         error_messages={'required': 'Digital address is required.'})
    def clean_victim_digital_address(self):
        victim_digital_address = self.cleaned_data.get('victim_digital_address')
        if not victim_digital_address:
            raise forms.ValidationError("Digital address cannot be empty.")
        return victim_digital_address


    victim_occupation = forms.CharField(label="Victim Occupation", max_length=100,
                                        error_messages={'required': 'Occupation is required.'})
    def clean_victim_occupation(self):
        victim_occupation = self.cleaned_data.get('victim_occupation')
        if not victim_occupation:
            raise forms.ValidationError("Occupation cannot be empty.")
        elif not re.match(r'^[a-zA-Z ]*$', victim_occupation):  # Allow spaces in occupations
            raise forms.ValidationError("Enter a valid occupation (letters and spaces only).")
        return victim_occupation


    victim_date_of_birth = forms.DateField(label="Victim Date of Birth", required=True, widget=forms.DateInput(attrs={'type': 'date'}),
                                        error_messages={'required': 'Date of birth is required.'})
    def clean_victim_date_of_birth(self):
        victim_date_of_birth = self.cleaned_data.get('victim_date_of_birth')
        if not victim_date_of_birth:
            raise forms.ValidationError("Date of birth cannot be empty.")
        return victim_date_of_birth

    
    location_of_incident = forms.CharField(label="Location of Incident", max_length=255, required=True,
                                           error_messages={'required': 'Location of the incident is required.'})
    def clean_location_of_incident(self):
        location_of_incident = self.cleaned_data.get('location_of_incident')
        if not location_of_incident:
            raise forms.ValidationError("Location of the incident cannot be empty.")
        return location_of_incident
    

    TYPE_OF_INCIDENT_CHOICES = [
        ('Theft', 'Theft'),
        ('Assault', 'Assault'),
        ('Traffic Accident', 'Traffic Accident'),
        ('Other', 'Other')]

    type_of_incident = forms.ChoiceField(
        label="Type of Incident",
        choices=TYPE_OF_INCIDENT_CHOICES,
        required=True,
        error_messages={'required': 'Type of incident is required.'}
    )
    def clean_type_of_incident(self):
        type_of_incident = self.cleaned_data.get('type_of_incident')
        if not type_of_incident:
            raise forms.ValidationError("Type of incident cannot be empty.")
        if type_of_incident not in dict(self.TYPE_OF_INCIDENT_CHOICES).keys():
            raise forms.ValidationError("Invalid type of incident selected.")
        return type_of_incident


    statement_of_incident = forms.CharField(label="Statement of Incident", widget=forms.Textarea, required=True,
                                        error_messages={'required': 'Statement of the incident is required.'})
    def clean_statement_of_incident(self):
        statement_of_incident = self.cleaned_data.get('statement_of_incident')
        if not statement_of_incident:
            raise forms.ValidationError("Statement of the incident cannot be empty.")
        return statement_of_incident
    

    key_witness_name = forms.CharField(label="Key Witness Name",max_length=255,required=False,
                                       error_messages={'invalid': 'Enter a valid witness name.'})
    def clean_key_witness_name(self):
        key_witness_name = self.cleaned_data.get('key_witness_name')
        if key_witness_name and not re.match(r'^[a-zA-Z\s]*$', key_witness_name):
            raise forms.ValidationError("Key witness name should only contain letters and spaces.")
        return key_witness_name


    key_witness_contact = forms.CharField(label="Key Witness Contact",max_length=20,required=False,
                                          widget=forms.TextInput(attrs={'placeholder': 'e.g., +1234567890'}),
                                          error_messages={'invalid': 'Enter a valid contact number.'})
    def clean_key_witness_contact(self):
        key_witness_contact = self.cleaned_data.get('key_witness_contact')
        if key_witness_contact:
            phone_pattern = re.compile(r'^\+?\d{7,15}$')
            if not phone_pattern.match(key_witness_contact):
                raise forms.ValidationError("Enter a valid phone number with 7 to 15 digits.")
        return key_witness_contact
    
    key_witness_physical_address = forms.CharField(label="Key Witness Physical Address",max_length=255,required=False,
                                                   error_messages={'invalid': 'Enter a valid physical address.'})
    def clean_key_witness_physical_address(self):
        key_witness_physical_address = self.cleaned_data.get('key_witness_physical_address')
        if key_witness_physical_address and not re.match(r'^[a-zA-Z0-9\s,]*$', key_witness_physical_address):
            raise forms.ValidationError("Physical address should only contain letters, numbers, spaces, and commas.")
        return key_witness_physical_address

    key_witness_digital_address = forms.CharField(label="Key Witness Digital Address",max_length=255,required=False,
                                                  error_messages={'invalid': 'Enter a valid digital address.'})
    def clean_key_witness_digital_address(self):
        key_witness_digital_address = self.cleaned_data.get('key_witness_digital_address')
        if key_witness_digital_address and not re.match(r'^[a-zA-Z0-9\s,]*$', key_witness_digital_address):
            raise forms.ValidationError("Digital address should only contain letters, numbers, spaces, and commas.")
        return key_witness_digital_address
    

# Step 2 Form: Incident Details and Statements
class CaseStep2Form(forms.Form):
    complainant_statement = forms.CharField(label="Complainant Statement", widget=forms.Textarea, required=True,
                                        error_messages={'required': 'Complainant statement is required.'})
    def clean_complainant_statement(self):
        complainant_statement = self.cleaned_data.get('complainant_statement')
        if not complainant_statement:
            raise forms.ValidationError("Complainant statement cannot be empty.")
        return complainant_statement
    

    suspect_statement = forms.CharField(label="Suspect Statement", widget=forms.Textarea, required=True,
                                    error_messages={'required': 'Suspect statement is required.'})
    def clean_suspect_statement(self):
        suspect_statement = self.cleaned_data.get('suspect_statement')
        if not suspect_statement:
            raise forms.ValidationError("Suspect statement cannot be empty.")
        return suspect_statement


    witness_statement = forms.CharField(label="Witness Statement", widget=forms.Textarea, required=True,
                                    error_messages={'required': 'Witness statement is required.'})
    def clean_witness_statement(self):
        witness_statement = self.cleaned_data.get('witness_statement')
        if not witness_statement:
            raise forms.ValidationError("Witness statement cannot be empty.")
        return witness_statement
    

    additional_witnesses = forms.CharField(label="Additional Witnesses", widget=forms.Textarea, required=False)
    def clean_additional_witnesses(self):
        additional_witnesses = self.cleaned_data.get('additional_witnesses')
        return additional_witnesses




# Step 3 Form: Reporting Officer and Case Progression
class CaseStep3Form(forms.Form):
    reporting_officer_name = forms.CharField(
        label="Reporting Officer Name", max_length=250, required=True,
        error_messages={'required': 'Reporting officer name is required.'}
    )
    def clean_reporting_officer_name(self):
        reporting_officer_name = self.cleaned_data.get('reporting_officer_name')
        if not reporting_officer_name:
            raise forms.ValidationError("Reporting officer name cannot be empty.")
        return reporting_officer_name

    reporting_officer_badge_id = forms.CharField(
        label="Badge ID", max_length=50, required=True,
        error_messages={'required': 'Badge ID is required.'}
    )
    def clean_reporting_officer_badge_id(self):
        reporting_officer_badge_id = self.cleaned_data.get('reporting_officer_badge_id')
        if not reporting_officer_badge_id:
            raise forms.ValidationError("Badge ID cannot be empty.")
        return reporting_officer_badge_id

    reporting_officer_rank = forms.CharField(
        label="Rank", max_length=100, required=True,
        error_messages={'required': 'Rank is required.'}
    )
    def clean_reporting_officer_rank(self):
        reporting_officer_rank = self.cleaned_data.get('reporting_officer_rank')
        if not reporting_officer_rank:
            raise forms.ValidationError("Rank cannot be empty.")
        return reporting_officer_rank

    reporting_officer_station = forms.CharField(
        label="Station", max_length=250, required=True,
        error_messages={'required': 'Station is required.'}
    )
    def clean_reporting_officer_station(self):
        reporting_officer_station = self.cleaned_data.get('reporting_officer_station')
        if not reporting_officer_station:
            raise forms.ValidationError("Station cannot be empty.")
        return reporting_officer_station

    reporting_officer_division = forms.CharField(
        label="Division", max_length=250, required=True,
        error_messages={'required': 'Division is required.'}
    )
    def clean_reporting_officer_division(self):
        reporting_officer_division = self.cleaned_data.get('reporting_officer_division')
        if not reporting_officer_division:
            raise forms.ValidationError("Division cannot be empty.")
        return reporting_officer_division

    charges_filed = forms.CharField(
        label="Charges Filed", widget=forms.Textarea, required=True,
        error_messages={'required': 'Charges filed are required.'}
    )
    def clean_charges_filed(self):
        charges_filed = self.cleaned_data.get('charges_filed')
        if not charges_filed:
            raise forms.ValidationError("Charges filed cannot be empty.")
        return charges_filed

    legal_actions_taken = forms.CharField(
        label="Legal Actions Taken", widget=forms.Textarea, required=True,
        error_messages={'required': 'Legal actions taken are required.'}
    )
    def clean_legal_actions_taken(self):
        legal_actions_taken = self.cleaned_data.get('legal_actions_taken')
        if not legal_actions_taken:
            raise forms.ValidationError("Legal actions taken cannot be empty.")
        return legal_actions_taken

    assigned_investigator = forms.CharField(
        label="Assigned Investigator", max_length=250, required=True,
        error_messages={'required': 'Assigned investigator is required.'}
    )
    def clean_assigned_investigator(self):
        assigned_investigator = self.cleaned_data.get('assigned_investigator')
        if not assigned_investigator:
            raise forms.ValidationError("Assigned investigator cannot be empty.")
        return assigned_investigator

    case_status = forms.CharField(
        label="Case Status", max_length=100, required=True,
        error_messages={'required': 'Case status is required.'}
    )
    def clean_case_status(self):
        case_status = self.cleaned_data.get('case_status')
        if not case_status:
            raise forms.ValidationError("Case status cannot be empty.")
        return case_status

    follow_up_required = forms.BooleanField(
        label="Follow-Up Required", required=False
    )

    additional_notes = forms.CharField(
        label="Additional Notes", widget=forms.Textarea, required=False
    )

    mugshot = forms.ImageField(
        label="Mugshot", required=True,
        error_messages={'required': 'Mugshot is required.'}
    )
    def clean_mugshot(self):
        mugshot = self.cleaned_data.get('mugshot')
        if mugshot and not mugshot.content_type.startswith('image/'):
            raise forms.ValidationError("Mugshot must be an image file.")
        return mugshot

    fingerprint = forms.FileField(
        label="Fingerprint", required=True,
        error_messages={'required': 'Fingerprint is required.'}
    )
    def clean_fingerprint(self):
        fingerprint = self.cleaned_data.get('fingerprint')
        if fingerprint and not fingerprint.content_type in ['image/png', 'image/jpeg']:
            raise forms.ValidationError("Fingerprint must be a PNG or JPEG file.")
        return fingerprint