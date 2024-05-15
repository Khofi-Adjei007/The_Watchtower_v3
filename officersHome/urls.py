from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('HomePage/', views.HomePage, name='HomePage'),
    path('officer_registrations/', views.officer_registrations, name='officer_registrations'),
]