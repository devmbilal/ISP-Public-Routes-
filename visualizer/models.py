from django.db import models

class RouteFile(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
