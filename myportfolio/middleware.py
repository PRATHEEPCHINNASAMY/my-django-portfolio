from django.urls import reverse
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            path_to_redirect = [reverse('myportfolio:register'), reverse('myportfolio:login')]
            if request.path  in path_to_redirect:
                return redirect('myportfolio:home')
            
        response  = self.get_response(request)
        return response
class RestrictUnauthenticatedUser:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        restricted_paths = [reverse("myportfolio:home")]

        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect('myportfolio:login')
        
        response  = self.get_response(request)
        return response