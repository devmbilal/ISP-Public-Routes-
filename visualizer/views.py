import os
import shutil
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RouteFileForm
from .models import RouteFile
from .create_network_graph import create_graph_from_csv, visualise_graph_map_folium_v2
import networkx as nx

def clear_media_directory():
    media_dir = settings.MEDIA_ROOT
    for filename in os.listdir(media_dir):
        file_path = os.path.join(media_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def upload_file(request):
    if request.method == 'POST':
        form = RouteFileForm(request.POST, request.FILES)
        if form.is_valid():
            clear_media_directory()  # Clear previous files before saving the new one
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
