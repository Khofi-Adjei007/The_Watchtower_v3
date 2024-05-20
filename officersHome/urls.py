from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('HomePage/', views.HomePage, name='HomePage'),
    path('CaseBox/', views.full_casebox_details, name='full_casebox_details'),
    path('officer_registrations/', views.officer_registrations, name='officer_registrations'),
    path('officer_login/', views.officer_login, name='officer_login'),
    path('officer_logout/', views.officer_logout, name='officer_logout'),
    path('queue_statement/', views.queue_statement, name='queue_statement'),
    path('drop_docket/', views.drop_docket, name='drop_docket'),
    path('preview_pdf/', views.preview_pdf, name='preview_pdf'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('save_pdf/', views.save_pdf, name='save_pdf'),
]