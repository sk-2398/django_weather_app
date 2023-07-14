from django.db import models

# Create your models here.
from django.db import models

class WeatherForecast(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    detailing_type = models.CharField(max_length=20)
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now_add=True,blank=True)
