# visualizer/views.py

import os
import shutil
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RouteFileForm
from .create_network_graph import create_graph_from_csv, visualise_graph_map_folium_v2
import networkx as nx

def clear_media_directory():
    """
    Clears the media directory of all files and subdirectories.
    """
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
    """
    Handles the file upload process, saves files to the media directory,
    creates a graph from the uploaded CSV files, and visualizes the graph.
    """
    if request.method == 'POST':
        form = RouteFileForm(request.POST, request.FILES)
        if form.is_valid():
            clear_media_directory()  # Clear previous files before saving the new ones
            files = request.FILES.getlist('csv_files')
            graph = nx.DiGraph()

            for f in files:
                # Save the file to the media directory
                file_path = os.path.join(settings.MEDIA_ROOT, f.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                # Process each CSV file
                graph = create_graph_from_csv(file_path, graph)
            
            # Visualize the graph with all routes
            visualise_graph_map_folium_v2(graph)
            return redirect('display_map')
    else:
        form = RouteFileForm()
    return render(request, 'upload.html', {'form': form})

def display_map(request):
    """
    Renders the map visualization template.
    """
    return render(request, 'graph_with_google_maps.html')
