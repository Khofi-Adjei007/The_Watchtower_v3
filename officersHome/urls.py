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
    path('', views.index, name='index'),
    path('register_docket/', views.register_docket, name='register_docket')
]