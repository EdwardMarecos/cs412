## hw/views.py
## description: write view functions to handle URL requests for the hw app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time, random

# Create your views here.

# def home(request):
#     """ handle the main url for the hw app"""

#     response_text = f'''
#     <html>
#     <h1>Hello, world!</h1>
#     <p>This is our first django web application!</p>
#     <hr>
#     This page was generated at {time.ctime()}.
#     </html>
#     '''

#     # create and return response to the client
#     return HttpResponse(response_text)

def home(request):
    """
    function to handle the url request for /hw (main page)
    delegate rendering to the template hw/home.html.
    """
    # use this template
    template_name = 'hw/home.html'
    
    # create a dict of context variables for the template
    context = {
        "current_time" : time.ctime(),
        "letter1" : chr(random.randint(65, 90)), # letter a ... z
        "letter2" : chr(random.randint(65, 90)), # same
        "number" : random.randint(1, 10), # number
    }

    # delegate rendering work to the template
    return render(request, template_name, context)