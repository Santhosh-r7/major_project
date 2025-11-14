# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageDraw
import io
import base64

from models.unet_model import build_unet  # custom U-Net builder
from rl_env import CropEnv  # RL environment (not used yet)
from utils import load_image, mask_to_overlay, get_weather_forecast, scrape_price_data

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit

# Load or build the U-Net model (weights file should be in backend/models/)
try:
    model = load_model('models/unet_model.h5', compile=False)
except Exception:
    # If no pre-trained model, build a fresh model (untrained) for interface
    model = build_unet(input_shape=(128,128,3), num_classes=1)

@app.route('/api/segment', methods=['POST'])
def segment():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Load and validate image
    img = load_image(file)
    if img is None:
        return jsonify({'error': 'Invalid image file'}), 400

    # Preprocess for model: resize and scale
    img_resized = img.resize((128, 128))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # batch dimension

    # Predict mask (assumes sigmoid output mask)
    pred_mask = model.predict(img_array)[0,...,0]
    mask = (pred_mask > 0.5).astype(np.uint8)  # binary mask

    # Compute severity: percentage of diseased pixels
    severity = float(mask.sum()) / mask.size * 100

    # Generate overlay image (disease areas in red)
    overlay_img = mask_to_overlay(img_resized, mask)

    # Encode overlay image to PNG base64
    buf = io.BytesIO()
    overlay_img.save(buf, format='PNG')
    overlay_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Simple treatment recommendation based on severity
    if severity > 50:
        recommendation = "High severity: apply fungicide and remove affected areas."
    elif severity > 20:
        recommendation = "Moderate severity: monitor closely and use preventive treatment."
    else:
        recommendation = "Low severity: standard care and observation."

    return jsonify({
        'severity': severity,
        'recommendation': recommendation,
        'overlay': f"data:image/png;base64,{overlay_b64}"
    })

@app.route('/api/forecast', methods=['POST'])
def forecast():
    data = request.get_json() or {}
    crop = data.get('crop')
    lat = data.get('lat')
    lon = data.get('lon')
    if not crop or lat is None or lon is None:
        return jsonify({'error': 'Crop name and coordinates required'}), 400

    # Fetch weather data (example using OpenWeatherMap)
    weather = get_weather_forecast(lat, lon)  # e.g., returns dict with relevant info

    # Scrape price data for the crop (placeholder example)
    price_info = scrape_price_data(crop)

    # Dummy transformer model predictions (stubbed)
    # In reality, here you'd use a trained model to predict future yield/price
    forecast = {
        'yield': {'3_months': 100, '6_months': 110, '12_months': 120},
        'price': {'3_months': price_info.get('3m', 200), 
                  '6_months': price_info.get('6m', 220), 
                  '12_months': price_info.get('12m', 250)}
    }

    return jsonify({
        'crop': crop,
        'weather': weather,
        'forecast': forecast
    })

if __name__ == '__main__':
    app.run(debug=True)
