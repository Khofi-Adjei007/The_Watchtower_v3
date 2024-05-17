# middlewares.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve



class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class RedirectOnBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            return response
        # Check if the requested URL requires login
        if resolve(request.path_info).url_name == 'HomePage':  # Replace 'HomePage' with your view name
            return redirect(settings.LOGIN_URL)
        return response