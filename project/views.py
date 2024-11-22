from django.shortcuts import render
from django.views.generic import *
from .models import *

# Create your views here.

class HomeView(TemplateView):
    template_name = 'project/home.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'project/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'project/category_detail.html'

class NoteListView(ListView):
    model = Note
    template_name = 'project/note_list.html'
    context_object_name = 'notes'

class NoteDetailView(DetailView):
    model = Note
    template_name = 'project/note_detail.html'