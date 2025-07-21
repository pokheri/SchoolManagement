#  The custom Middleware 
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import resolve

class CustomMiddleWare:

    def __init__(self, get_response):
        print('the middleware is initilized we are here in the custom middleware ')
        self.get_response = get_response
        self.counter   = 0 
        # initilized at once 

    def __call__(self,request,  *args, **kwds):
        
        print('before calling the view ')
        response = self.get_response(request)
        print('after reponse ')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # print('we are in the view  process view and checking what might happend ')
        # return HttpResponse(' The view is short circuited and now it cant reach the original location ' )
        return None # for the normal floww, it will execute next the view 
    
    def process_exception(self, request, exception):
        print('the exception we got here ')
        print(exception)

        return HttpResponse('hey there is an exception in the program ')

    def process_template_response(self, request, response):
        # it again started the middle chaining from the bottom to the up 
        return # the rendered template  
    
class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self,request,  *args, **kwds):

        path = resolve(request.path_info).url_name
        if not request.user.is_authenticated  and path!='login':
            return redirect('login')
        response = self.get_response(request)
        return response

