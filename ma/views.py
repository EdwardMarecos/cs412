from typing import Any
from django.shortcuts import render

# Create your views here.

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result

import plotly
import plotly.graph_objects as go


class ResultsListView(ListView):
    '''View to display marathon results'''
    template_name = 'ma/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('place_overall')
        # filter results by these field(s):
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if Result.first_name:
                qs = qs.filter(city=city)
                
        return qs
    
class ResultDetailView(DetailView):
    """display a single result on its own page"""

    template_name = 'ma/result_detail.html'
    model = Result
    context_object_name = 'r'

    # implement some methods
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        # get superclass version of context
        context = super().get_context_data(**kwargs)
        r = context['r']

        #  get data half marathon splits
        first_half_seconds = (r.time_half1.hour * 60 + 
                              r.time_half1.minute * 60 + 
                              r.time_half1.second)

        second_half_seconds = (r.time_half2.hour * 60 + 
                              r.time_half2.minute * 60 + 
                              r.time_half2.second)
        
        # build pie chart
        x = ["first half time", "second half time"]
        y = [first_half_seconds, second_half_seconds]
        print(f'x={x}')
        print(f'y={y}')
        fig = go.Pie(labels=x, values=y) 
        title_text = f"half marathon splits"
        pie_div = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        # add pie chart to context
        context['pie_div'] = pie_div

        # create graph of runners who passed/passed by
        x= [f'Runners Passed by {r.first_name}', f'Runners who Passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        
        fig = go.Bar(x=x, y=y)
        title_text = f"Runners Passed/Passed By"
        graph_div_passed = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",
                                         
                                         ) 
        context['graph_div_passed'] = graph_div_passed

        return context