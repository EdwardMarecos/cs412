## restaurant/views.py
## description: write view functions to handle URL requests for the restaurant app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse#, redirect
import time, random

# Create your views here.

items = ["hi",
         "bye",
         "sigh"]

def base(request):
    """
    the page with basic information about the restaurant
    """
    template_name = 'restaurant/base.html'
    return render(request, template_name)

def main(request):
    """
    the page with basic information about the restaurant
    """
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    """
    display an online order form
    """
    # use this template
    template_name = 'restaurant/order.html'
    
    # create a dict of context variables for the template
    restaurant_context = {
        "daily_special" : items[random.randint(0, len(items)-1)], # random quote
    }

    # delegate rendering work to the template
    return render(request, template_name, restaurant_context)

def confirmation(request):
    """
    a confirmation page to display after the order is placed
    handle form submission
    """
    # use this template
    template_name = 'restaurant/confirmation.html'
    
    # create a dict of context variables for the template
    # show_all_context = {
    #     "conf_time" : time.ctime(), # a random time 30 - 60 min after current time/date
    #     #edit this
    # }
    print(request)

    # check that we have a post request
    if request.POST:
        #read the form data into python variables
        name = request.POST['name']

        context = {
            'name': name,
        }

        # delegate rendering work to the template
        return render(request, template_name, context=context)
    
    ## handle get request on this url
    return HttpResponse("Nope")

    # template_name = "formdata/form.html"
    # return render(request, template_name)

    # return redirect("order")