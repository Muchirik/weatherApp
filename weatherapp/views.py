from django.shortcuts import render
import requests,json
from . models import City
from . forms import CityForm

# Create your views here.
def index(request):
    cities = City.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0c8ca0134cd7534aaf34fdca3a003878'
    
    search_result = None
    background_image = 'https://source.unsplash.com/1600x900/?weather'  # Default background image
    if request.method == 'POST':
        if 'search' in request.POST:  # Handle search functionality
            city_name = request.POST.get('search')
            city_weather = requests.get(url.format(city_name)).json()
            if city_weather.get('cod') == 200:  # Check if the API response is successful
                condition = city_weather['weather'][0]['main'].lower()
                search_result = {
                    'city': city_name,
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon'],
                    'condition': condition
                }
                # Set background image based on weather condition
                if condition == 'rain':
                    background_image = 'https://source.unsplash.com/1600x900/?rain'
                elif condition == 'clear':
                    background_image = 'https://source.unsplash.com/1600x900/?sunny'
                elif condition == 'clouds':
                    background_image = 'https://source.unsplash.com/1600x900/?cloudy'
                elif condition == 'snow':
                    background_image = 'https://source.unsplash.com/1600x900/?snow'
                else:
                    background_image = 'https://unsplash.com/photos/AgAvN9cBfoo'  # Fallback image
        else:  # Handle adding a new city
            form = CityForm(request.POST)
            form.save()
    
    form = CityForm()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        
        if city_weather.get('cod') != 200:  # Check if the API response is successful
            continue  # Skip this city if there's an error in the response
        
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form, 'search_result': search_result, 'background_image': background_image}
    return render(request, 'weatherapp/index.html', context)  # returns index.html template
