from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import queue_statement, check_session, clear_session, verify_badge



urlpatterns = [
    path('queue_statement/', views.queue_statement, name='queue_statement'),
    path('check_session/', views.check_session, name='check_session'),
    path('clear_session/', views.clear_session, name='clear_session'),
    path('preview_pdf/', views.preview_pdf, name='preview_pdf'),
    path('save_pdf/', views.save_pdf, name='save_pdf'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('HomePage/', views.HomePage, name='HomePage'),
    path('CaseBox/', views.full_casebox_details, name='full_casebox_details'),
    path('officer_registrations/', views.officer_registrations, name='officer_registrations'),
    path('officer_login/', views.officer_login, name='officer_login'),
    path('officer_logout/', views.officer_logout, name='officer_logout'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('selectPurpose/', views.selectPurpose, name='selectPurpose'),
    path('docketforms/', views.docketforms, name='docketforms'),
    path('searchdatabase/', views.searchdatabase, name='searchdatabase'),
    path('casesProgress/', views.casesProgress, name='casesProgress'),
    path('commandmessaging/', views.commandmessaging, name='commandmessaging'),
    path('docketforms/CaseStep1Form/', views.CaseStep1Form, name='CaseStep1Form'),
    path('docketforms/CaseStep2Form/', views.CaseStep2Form, name='CaseStep2Form'),
    path('docketforms/CaseStep3Form/', views.CaseStep3Form, name='CaseStep3Form'),
    path('verify_badge/', verify_badge, name='verify_badge'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
