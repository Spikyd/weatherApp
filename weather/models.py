from django.db import models

class Forecast(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=100)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    total_precip = models.FloatField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    condition = models.CharField(max_length=255) 
    wind_speed = models.FloatField()              
    humidity = models.IntegerField()              
    uv = models.FloatField()                      

    class Meta:
        unique_together = ('date', 'city')

    def __str__(self):
        return f'{self.city} - {self.date}'
