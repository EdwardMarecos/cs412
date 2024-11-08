from datetime import datetime
from typing import Any
from django.shortcuts import render

# Create your views here.

from django.db.models.query import QuerySet
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter

import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



# Create your views here.
class VoterListView(ListView):
    '''View to display voter records'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        # Start with the entire queryset
        qs = super().get_queryset().order_by('id')

        # Apply filters based on the GET parameters
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Apply the filters only if they are specified
        if party:
            qs = qs.filter(party=party)
        
        if min_dob:
            qs = qs.filter(dob__year__gte=min_dob)
        
        if max_dob:
            qs = qs.filter(dob__year__lte=max_dob)
        
        if voter_score:
            qs = qs.filter(voter_score=voter_score)

        # Check if the voter participated in specific elections
        if self.request.GET.get('voted_20state'):
            qs = qs.filter(v20state=True)
        
        if self.request.GET.get('voted_21town'):
            qs = qs.filter(v21town=True)
        
        if self.request.GET.get('voted_21primary'):
            qs = qs.filter(v21primary=True)
        
        if self.request.GET.get('voted_22general'):
            qs = qs.filter(v22general=True)
        
        if self.request.GET.get('voted_23town'):
            qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = datetime.now().year

        # Adding dynamic year range for the drop-down list
        context['years'] = range(1900, current_year + 1)

        # Adding voter scores for filtering
        context['voter_scores'] = range(0, 6)

        return context

class VoterDetailView(DetailView):
    '''View to display details for a single voter'''
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = context['voter']
        
        # Add leading zeros to ZIP code if needed
        if voter.address_zipcode:
            voter.address_zipcode = str(voter.address_zipcode).zfill(5)
        
        return context

class VoterGraphsView(ListView):
    '''View to display graphs about voter records'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        # Start with the entire queryset
        qs = super().get_queryset()

        # Apply filters based on the GET parameters
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')

        # Apply the filters only if they are specified
        if party:
            qs = qs.filter(party=party)
        
        if min_dob:
            qs = qs.filter(dob__year__gte=min_dob)
        
        if max_dob:
            qs = qs.filter(dob__year__lte=max_dob)
        
        if voter_score:
            qs = qs.filter(voter_score=voter_score)

        # Check if the voter participated in specific elections
        if self.request.GET.get('voted_20state'):
            qs = qs.filter(v20state=True)
        
        if self.request.GET.get('voted_21town'):
            qs = qs.filter(v21town=True)
        
        if self.request.GET.get('voted_21primary'):
            qs = qs.filter(v21primary=True)
        
        if self.request.GET.get('voted_22general'):
            qs = qs.filter(v22general=True)
        
        if self.request.GET.get('voted_23town'):
            qs = qs.filter(v23town=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters_qs = self.get_queryset()

        # Add year and voter score ranges for the search form
        current_year = datetime.now().year
        context['years'] = range(1900, current_year + 1)
        context['voter_scores'] = range(0, 6)

        # Convert filtered queryset to DataFrame
        voters = voters_qs.values('dob', 'party', 'v20state', 'v21town', 'v21primary', 'v22general', 'v23town')
        df = pd.DataFrame(list(voters))  # Convert queryset to a DataFrame

        # Ensure 'dob' is a datetime type and extract year
        if 'dob' in df:
            df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
            df['year_of_birth'] = df['dob'].dt.year

        # Check if the DataFrame is empty to avoid errors
        if df.empty:
            context['histogram_div'] = "No data available"
            context['pie_div'] = "No data available"
            context['election_div'] = "No data available"
            return context

        # Histogram: Voter distribution by year of birth
        if 'year_of_birth' in df:
            birth_year_counts = df['year_of_birth'].value_counts().sort_index()
            fig_histogram = px.bar(
                x=birth_year_counts.index,
                y=birth_year_counts.values,
                labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
                title=f"Voter distribution by Year of Birth (n={len(df)})"
            )
            histogram_div = plotly.offline.plot(fig_histogram, auto_open=False, output_type='div')
            context['histogram_div'] = histogram_div

        # Pie Chart: Voter distribution by party affiliation
        party_counts = df['party'].value_counts()
        fig_pie = px.pie(
            names=party_counts.index,
            values=party_counts.values,
            title=f"Voter distribution by Party Affiliation (n={len(df)})",
            labels={'names': 'Party', 'values': 'Count'}
        )
        pie_div = plotly.offline.plot(fig_pie, auto_open=False, output_type='div')
        context['pie_div'] = pie_div

        # Bar Chart: Voter participation in elections
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        vote_counts = [df[election].sum() for election in elections if election in df]
        fig_election = px.bar(
            x=elections,
            y=vote_counts,
            labels={'x': 'Election', 'y': 'Number of Voters'},
            title=f"Vote Count by Election (n={len(df)})"
        )
        election_div = plotly.offline.plot(fig_election, auto_open=False, output_type='div')
        context['election_div'] = election_div

        return context




    


