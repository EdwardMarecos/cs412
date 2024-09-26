## restaurant/views.py
## description: write view functions to handle URL requests for the restaurant app

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import time, random
import datetime
mydate = datetime.datetime.now()

logo = ["https://thumbs.dreamstime.com/b/cute-red-cat-drinking-peach-coffee-tea-front-coffee-shop-cartoon-illustration-generative-ai-illustration-cute-cat-271960767.jpg"]

daily_specials = {
    "Peach Mochi": 5.00,
    "Peach Cheese Mousse Cake": 6.50,
    "Peach Slush": 4.50,
    "Peach Cobbler": 5.75
}

regular_menu = {
    "Peach Latte": 4.00,
    "Peach Tea": 3.00,
    "Peach Crepe": 7.00,
    "Peach Boba": 5.50
}

peach_boba_addons = {
    'Tapioca Pearls': 0.50,
    'Popping Boba': 0.75,
    'Lychee Jelly': 0.60,
    'Aloe Vera': 0.70,
    'Extra Peach Syrup': 0.40,
    'Coconut Milk': 0.80,
    'Oat Milk': 0.90,
    'More Ice': 0.00,
    'Less Ice': 0.00,
    'No Ice': 0.00,
    'Extra Sweet': 0.20,
    'Half Sweet': 0.00,
}


ran_time = mydate.strftime("%b") + time.strftime(" %d %Y at %I:%M %p", time.localtime(time.time()+random.randrange(60, 6000)))

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

    main_context = {
        "peachtree_cafe" : logo[0]
    }
    return render(request, template_name, main_context)

def order(request):
    """
    display an online order form
    """
    # use this template
    template_name = 'restaurant/order.html'
    random_special = random.choice(list(daily_specials.items()))
    # create a dict of context variables for the template
    restaurant_context = {
        "daily_special" : random_special,
        "regular_menu" : regular_menu,
        "peach_boba_addons": peach_boba_addons,
    }

    # delegate rendering work to the template
    return render(request, template_name, restaurant_context)

def confirmation(request):
    """
    A confirmation page to display after the order is placed.
    """
    template_name = 'restaurant/confirmation.html'

    if request.method == "POST":
        # Get the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        requests = request.POST.get('requests', '')  # Get special requests, default to empty string if not filled

        # Get the ordered items (from daily special and regular menu)
        ordered_items = request.POST.getlist('item')

        # Get the add-ons for Peach Boba (if any were selected)
        addons = request.POST.getlist('addon')

        # Calculate the total price
        total_price = 0.0
        ordered_list = []

        # Add prices for daily specials and regular menu items
        for item in ordered_items:
            if item in daily_specials:
                ordered_list.append(f"{item} - ${daily_specials[item]:.2f}")
                total_price += daily_specials[item]
            elif item in regular_menu:
                ordered_list.append(f"{item} - ${regular_menu[item]:.2f}")
                total_price += regular_menu[item]

        # Add prices for any add-ons
        addon_list = []
        for addon in addons:
            if addon in peach_boba_addons:
                addon_list.append(f"{addon} - ${peach_boba_addons[addon]:.2f}")
                total_price += peach_boba_addons[addon]

        # Pass all necessary data to the context
        context = {
            "conf_time": ran_time,  # Random pickup time
            "name": name,
            "email": email,
            "ordered_items": ordered_list,
            "addons": addon_list,
            "total_price": total_price,
            "requests": requests,  # Pass special requests to the context
            "phone": phone,
        }

        # Render the confirmation page with the order details
        return render(request, template_name, context=context)

    # return HttpResponse("Invalid request")

    return redirect("order")