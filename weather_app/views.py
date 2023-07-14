from django.shortcuts import render
from datetime import datetime
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WeatherForecast
from .serializers import WeatherForecastSerializer
import requests
import datetime
from django.conf import settings

class WeatherForecastView(APIView):
    def get(self, request):
        # lat = 48.8566
        # lon = 2.3522
        # detailing_type = "current"
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        detailing_type = request.GET.get('detailing_type')

        # Check if the data is available in the local DB
        weather_forecast = WeatherForecast.objects.filter(
            lat=lat,
            lon=lon,
            detailing_type=detailing_type,
            last_updated__gte=datetime.datetime.now() - datetime.timedelta(minutes=settings.TIME_SENSITIVE_MINUTES)
        ).first()
        
        if weather_forecast:
            # Return data from the local DB
            serializer = WeatherForecastSerializer(weather_forecast)
            return Response(serializer.data)
        else:
            # Request data from OpenWeatherMap API
            api_key = 'Add your API key here'
            # api_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily&appid={api_key}'
            api_url= f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()

                # Save the data to the local DB
                weather_forecast = WeatherForecast.objects.create(
                    lat=lat,
                    lon=lon,
                    detailing_type=detailing_type,
                    data=data
                )

                serializer = WeatherForecastSerializer(weather_forecast)
               
                
                return Response(serializer.data,status=200)
            else:
                return Response({'error': 'Failed to retrieve weather forecast data'},status=401)
            

def homeview(request):
    if request.method == 'POST':
        lat = (request.POST.get('lat')).replace(" ","")
        lon = request.POST.get('lon').replace(" ","")
        detailing_type = request.POST.get('detailing_type')

        api_url = 'http://127.0.0.1:8000/api/weather-forecast/'  # Replace with your API endpoint URL
        params = {'lat': lat, 'lon': lon, 'detailing_type':detailing_type}
        response = requests.get(api_url, params=params)
        
        data = response.json()

        if response.status_code==200:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%A, %I:%M %p")
            temp=(data['data']['main']['temp']-273.15)
            iconurl = "http://openweathermap.org/img/w/" + data['data']['weather'][0]['icon'] + ".png"
        
            context={
                'location':data['data']['name'],
                'temp':round(temp,2),
                'humidity':data['data']['main']['humidity'],
                'wind_speed' : data['data']['wind']['speed'],
                'weather':data['data']['weather'][0]['description'],
                'icon':iconurl,
                'datetime':formatted_datetime,
                'show':True,
                'error':False
            }
        else:
            context={
                'show':False,

                'error':True
            }
        
        return render(request, 'home.html', context=context)
    else:
        context={
            'show':False,
            'error':False

        }
        return render(request, 'home.html',context=context)