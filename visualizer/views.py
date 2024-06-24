import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RouteFileForm
from .models import RouteFile
from .create_network_graph import create_graph_from_csv, visualise_graph_map_folium_v2
import networkx as nx

def upload_file(request):
    if request.method == 'POST':
        form = RouteFileForm(request.POST, request.FILES)
        if form.is_valid():
            route_file = form.save()
            # Process the file
            process_csv_file(route_file.csv_file.path)
            return redirect('display_map')
    else:
        form = RouteFileForm()
    return render(request, 'upload.html', {'form': form})

def display_map(request):
    return render(request, 'graph_with_google_maps.html')

def process_csv_file(file_path):
    # Function to process CSV and create HTML file
    graph = nx.DiGraph()
    graph = create_graph_from_csv(file_path, graph)
    visualise_graph_map_folium_v2(graph)
