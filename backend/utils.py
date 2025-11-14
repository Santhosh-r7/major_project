# backend/utils.py
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import requests
from bs4 import BeautifulSoup

ALLOWED_EXT = {'png', 'jpg', 'jpeg'}

def load_image(file):
    """Load an image file via PIL, ensuring it has a valid extension."""
    filename = file.filename.lower()
    if '.' not in filename or filename.rsplit('.', 1)[1] not in ALLOWED_EXT:
        return None
    try:
        img = Image.open(file.stream).convert('RGB')
        return img
    except Exception:
        return None

def mask_to_overlay(image, mask):
    """Overlay a binary mask (numpy array) onto a PIL image (RGB) as red highlight."""
    overlay = image.convert('RGBA')
    mask_img = Image.fromarray((mask * 255).astype('uint8')).resize(image.size)
    red_mask = Image.new('RGBA', image.size, (255, 0, 0, 125))
    overlay.paste(red_mask, (0,0), mask_img)
    return overlay

def get_weather_forecast(lat, lon):
    """Fetch basic weather info from OpenWeatherMap (must set OWM_API_KEY)."""
    API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()  # as shown in example code:contentReference[oaicite:3]{index=3}
        main = data.get('main', {})
        wind = data.get('wind', {})
        return {
            'temp': main.get('temp'),
            'pressure': main.get('pressure'),
            'humidity': main.get('humidity'),
            'wind_speed': wind.get('speed'),
            'description': data.get('weather',[{}])[0].get('description')
        }
    except Exception:
        return {}

def scrape_price_data(crop_name):
    """
    Placeholder function: scrapes a commodity price page for the given crop.
    Here we simulate scraping logic (in practice, parse real HTML).
    """
    # Example using BeautifulSoup (pattern from price scraping :contentReference[oaicite:4]{index=4})
    example_html = "<table><tr><td>Crop</td><td>3m</td><td>6m</td><td>12m</td></tr>" \
                   f"<tr><td>{crop_name}</td><td>180</td><td>190</td><td>200</td></tr></table>"
    soup = BeautifulSoup(example_html, 'html.parser')
    row = soup.find('tr', text=lambda t: t and crop_name in t)
    prices = {'3m': 0, '6m': 0, '12m': 0}
    if row:
        cells = [td.get_text() for td in row.find_all('td')]
        # Expecting [crop, 3m, 6m, 12m]
        if len(cells) >= 4:
            prices['3m'], prices['6m'], prices['12m'] = cells[1], cells[2], cells[3]
    return prices
