# from django.db import models
# from django.db import models
# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import MinLengthValidator


# # Create your models here.
# class OfficerLogin(models.Model):
#     username = models.CharField(unique=True, max_length=250)
#     password = models.CharField(max_length=256)  # Increase max_length for password


# class NewOfficerRegistration(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
#     first_name = models.CharField(max_length=250)
#     middle_name = models.CharField(max_length=250)
#     last_name = models.CharField(max_length=250)
    
#     username = models.CharField(max_length=250, unique=True, validators=[MinLengthValidator(1)])
#     def save(self, *args, **kwargs):
#         if not self.username.strip():
#             raise ValueError("Username cannot be empty")
#         super().save(*args, **kwargs)

#     OFFICER_GENDER_CHOICES_MALE = 'M'
#     OFFICER_GENDER_CHOICES_FEMALE = 'F'

#     OFFICER_GENDER_CHOICES = [
#         (OFFICER_GENDER_CHOICES_MALE, 'Male'),
#         (OFFICER_GENDER_CHOICES_FEMALE, 'Female'),
        
#         ]
#     officer_gender = models.CharField(max_length=250, choices=OFFICER_GENDER_CHOICES, default='')
#     email = models.EmailField(unique=True, max_length=250)
#     phone_contact = models.IntegerField(unique=True)
#     officer_address = models.CharField(max_length=250)
    
#     # Constants for officer ranks
#     RANK_Constable = 'Constable'
#     RANK_Lance_Corporal = 'Lance Corporal'
#     RANK_Corporal = 'Corporal'
#     RANK_Sergeant = 'Sergeant'
#     RANK_District_Sergeant_Major = 'District Sergeant Major'
#     RANK_Inspector = 'Inspector'
#     RANK_Regional_Sergeant_Major = 'Regional Sergeant Major'
#     RANK_Chief_Inspector = 'Chief Inspector'
#     RANK_Assistant_Superintendent_of_Police = 'Assistant Superintendent of Police'
#     RANK_Deputy_Superintendent_of_Police = 'Deputy Superintendent of Police'
#     RANK_Superintendent_of_Police = 'Superintendent of Police'
#     RANK_Chief_Superintendent = 'Chief Superintendent'
#     RANK_Assistant_Commissioner_of_Police = 'Assistant Commissioner of Police'
#     RANK_Deputy_Commissioner_of_Police = 'Deputy Commissioner of Police'
#     RANK_Commissioner_of_Police = 'Commissioner of Police'
#     RANK_Inspector_General_of_Police = 'Inspector General of Police'

#     # Choices for officer ranks
#     OFFICER_RANK_CHOICES = [
#         (RANK_Constable, 'Constable'),
#         (RANK_Lance_Corporal, 'Lance Corporal'),
#         (RANK_Corporal, 'Corporal'),
#         (RANK_Sergeant, 'Sergeant'),
#         (RANK_District_Sergeant_Major, 'District Sergeant Major'),
#         (RANK_Inspector, 'Inspector'),
#         (RANK_Regional_Sergeant_Major, 'Regional Sergeant Major'),
#         (RANK_Chief_Inspector, 'Chief Inspector'),
#         (RANK_Assistant_Superintendent_of_Police, 'Assistant Superintendent of Police'),
#         (RANK_Deputy_Superintendent_of_Police, 'Deputy Superintendent of Police'),
#         (RANK_Superintendent_of_Police, 'Superintendent of Police'),
#         (RANK_Chief_Superintendent, 'Chief Superintendent'),
#         (RANK_Assistant_Commissioner_of_Police, 'Assistant Commissioner of Police'),
#         (RANK_Deputy_Commissioner_of_Police, 'Deputy Commissioner of Police'),
#         (RANK_Commissioner_of_Police, 'Commissioner of Police'),
#         (RANK_Inspector_General_of_Police, 'Inspector General of Police'),
#     ]
#     officer_current_rank = models.CharField(max_length=250, choices=OFFICER_RANK_CHOICES)

#     officer_current_station = models.CharField(max_length=250)
#     officer_staff_ID = models.CharField(unique=True, max_length=250)
    
#     EDUCATION_WASSCE = 'WS'
#     EDUCATION_DEGREE = 'DG'
#     EDUCATION_MASTERS = 'MS'
#     EDUCATION_PHD = 'PH'
    
#     EDUCATION_QUALIFICATION_CHOICES = [
#         (EDUCATION_WASSCE, 'WASSCE'),
#         (EDUCATION_DEGREE, 'DEGREE'),
#         (EDUCATION_MASTERS, 'MASTERS'),
#         (EDUCATION_PHD, 'PHD'),
#     ]
#     officer_qualification = models.CharField(max_length=250, choices=EDUCATION_QUALIFICATION_CHOICES)
#     officer_date_of_birth = models.DateField()
#     officer_operations_region = models.CharField(max_length=250)

#         # Constants for officer departments
#     DEPARTMENT_Criminal_InvestigationDepartment = 'CID'
#     DEPARTMENT_Motor_Traffic_and_TransportDirectorate = 'MTTD'
#     DEPARTMENT_Domestic_Violence_and_Victim_Support_Unit = 'DOVVSU'
#     DEPARTMENT_The_Police_College = 'The Police College'
#     DEPARTMENT_Other_Training_Institutions = 'Other Training Institutions'
#     DEPARTMENT_Works_and_Housing_Department = 'W&H'
#     DEPARTMENT_Public_Relations_Department = 'PRD'
#     DEPARTMENT_Medical_Hospital = 'MH'
#     DEPARTMENT_Marine_Ports_and_Railways = 'Marine Ports & Railways'
#     DEPARTMENT_Community_Policing = 'Community Policing'

#         # Choices for officer departments
#     OFFICER_DEPARTMENT_CHOICES = [
#             (DEPARTMENT_Criminal_InvestigationDepartment, 'Criminal Investigation Department [CID]'),
#             (DEPARTMENT_Motor_Traffic_and_TransportDirectorate, 'Motor Traffic and Transport Directorate [MTTD]'),
#             (DEPARTMENT_Domestic_Violence_and_Victim_Support_Unit, 'Domestic Violence and Victim Support Unit [DOVVSU]'),
#             (DEPARTMENT_The_Police_College, 'The Police College'),
#             (DEPARTMENT_Other_Training_Institutions, 'Other Training Institutions'),
#             (DEPARTMENT_Works_and_Housing_Department, 'Works & Housing Department'),
#             (DEPARTMENT_Public_Relations_Department, 'Public Relations Department'),
#             (DEPARTMENT_Medical_Hospital, 'Medical – Hospital'),
#             (DEPARTMENT_Marine_Ports_and_Railways, 'Marine Ports & Railways'),
#             (DEPARTMENT_Community_Policing, 'Community Policing'),
#         ]

#     officer_operations_department = models.CharField(max_length=250, choices=OFFICER_DEPARTMENT_CHOICES)
#     officer_profile_image = models.ImageField(upload_to='')
#     password = models.CharField(max_length=128)



# class ChargeOfficer(NewOfficerRegistration):
#     ability_to_make_report = models.BooleanField(default=False)


# class StationOfficer(NewOfficerRegistration):
#     assigned_duties = models.TextField()


# class CIDCrimeOfficer(NewOfficerRegistration):
#     registered_docket = models.TextField()
#     locked_docket = models.BooleanField(default=False)
# #


# # Target models
# class Target(models.Model):
#     name = models.CharField(max_length=255)
#     residential_address = models.CharField(max_length=255)
#     gps = models.CharField(max_length=100)
#     contact = models.CharField(max_length=100)
#     gender = models.CharField(max_length=10)
#     date_of_birth = models.DateField()
#     age = models.IntegerField()
#     work_occupation = models.CharField(max_length=255)
#     placeOfWork = models.CharField(max_length=255)
#     hometown = models.CharField(max_length=255)
#     material_evidendence = models.FileField(upload_to='evidence/')


# class Victim(Target):
#     pass


# class Suspect(Target):
#     mugshot = models.ImageField(upload_to='mugshots/')
#     fingerprints = models.ImageField(upload_to='fingerprints/')
#     life_details = models.TextField()


# class Witness(Target):
#     relationship_to_witness = models.CharField(max_length=100)