## quotes/views.py
## description: write view functions to handle URL requests for the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time, random

# Create your views here.

quotes = ["It is good to love many things, for therein lies the true strength, and whosoever loves much performs much, and can accomplish much, and what is done in love is well done.” \n― Vincent Van Gogh", 
          "I dream my painting and I paint my dream.”\n― Vincent Van Gogh",
          "Be clearly aware of the stars and infinity on high. Then life seems almost enchanted after all.”\n― Vincent Van Gogh",
          "...and then, I have nature and art and poetry, and if that is not enough, what is enough?”\n― Vincent Van Gogh",
          "There is nothing more truly artistic than to love people.”\n― Vincent Van Gogh",
          "A great fire burns within me, but no one stops to warm themselves at it, and passers-by only see a wisp of smoke”\n― Vincent Van Gogh",
          "I don't know anything with certainty, but seeing the stars makes me dream.”\n― Vincent Van Gogh",
          "I put my heart and soul into my work, and I have lost my mind in the process.”\n― Vincent Van Gogh",
          "I often think that the night is more alive and more richly colored than the day.”\n― Vincent Van Gogh",
          "The sadness will last forever.”\n― Vincent Van Gogh"]
images = ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIKgYo2LCnA_K-Zp7li4uqWMnFgtdgmIM7XA&s",
          "https://images.pexels.com/photos/4218701/pexels-photo-4218701.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
          "https://st2.depositphotos.com/1757635/7119/i/450/depositphotos_71195665-stock-photo-small-girl-with-umbrella.jpg",
          "https://bluefoxmusic.com/wp-content/uploads/2023/09/Art-BFM053-SecretsOfSuccess.png",
          "https://cdn.britannica.com/78/43678-050-F4DC8D93/Starry-Night-canvas-Vincent-van-Gogh-New-1889.jpg",
          "https://t4.ftcdn.net/jpg/05/63/67/45/360_F_563674524_3o22Tip6FKFTR0y1PynnFekxkIJvNlnO.jpg",
          "https://cdn.britannica.com/78/69678-050-491A5ED8/Bedroom-oil-canvas-Vincent-van-Gogh-Art-1889.jpg",
          "https://www.worldhistory.org/img/r/p/500x600/15460.png?v=1723002848",
          "https://artofericwayne.com/wp-content/uploads/2016/12/vincent-eyes-for-blog.jpg?w=1400",
          "https://wallpapers.com/images/hd/van-gogh-1800-x-1200-background-hqqbe3rkj0kw3vt6.jpg"]

def base(request):
    """
    Function to handle the request for the homepage.
    """
    template_name = 'quotes/base.html'
    return render(request, template_name)

def quote(request):
    """
    function to handle the url request for /quote (main page)
    delegate rendering to the template quotes/quote.html.
    directs the application to display one quote and one image
    """
    # use this template
    template_name = 'quotes/quote.html'
    
    # create a dict of context variables for the template
    quote_context = {
        "quote1" : quotes[random.randint(0, len(quotes)-1)], # random quote
        "image1" : images[random.randint(0, len(images)-1)]  # random image 
    }

    # delegate rendering work to the template
    return render(request, template_name, quote_context)

def show_all(request):
    """
    function to handle the url request for /show_all (other page)
    delegate rendering to the template quotes/show_all.html.
    add the entire list of quotes and images to the context data for the view
    """
    # use this template
    template_name = 'quotes/show_all.html'
    
    # create a dict of context variables for the template
    show_all_context = {
        "quotes" : quotes, # all quotes
        "images" : images, # all images
    }

    # delegate rendering work to the template
    return render(request, template_name, show_all_context)

def about(request):
    """
    function to handle the url request for /about (ancillary page)
    delegate rendering to the template quotes/about.html.
    display information about the famous person whose quotes are shown in this application
    and credit to you - i.e. me
    """
    # use this template
    template_name = 'quotes/about.html'

    # delegate rendering work to the template
    return render(request, template_name)