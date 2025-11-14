// frontend/src/components/ForecastPage.jsx
import React, { useState } from 'react';
import axios from 'axios';

function ForecastPage() {
  const [crop, setCrop] = useState('');
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');
  const [forecast, setForecast] = useState(null);
  const [weather, setWeather] = useState(null);

  const handleSubmit = () => {
    if (!crop || !lat || !lon) {
      alert('Please enter crop name and coordinates.');
      return;
    }
    axios.post('/api/forecast', { crop, lat, lon })
      .then(res => {
        setWeather(res.data.weather);
        setForecast(res.data.forecast);
      })
      .catch(err => {
        console.error(err);
        alert('Error fetching forecast');
      });
  };

  return (
    <div>
      <h3>Crop Yield and Price Forecast</h3>
      <div className="mb-2">
        <input 
          type="text" placeholder="Crop Name" 
          value={crop} onChange={e => setCrop(e.target.value)} 
          className="form-control"
        />
      </div>
      <div className="mb-2">
        <input 
          type="number" placeholder="Latitude" 
          value={lat} onChange={e => setLat(e.target.value)} 
          className="form-control"
        />
      </div>
      <div className="mb-2">
        <input 
          type="number" placeholder="Longitude" 
          value={lon} onChange={e => setLon(e.target.value)} 
          className="form-control"
        />
      </div>
      <button className="btn btn-success" onClick={handleSubmit}>Get Forecast</button>

      {forecast && (
        <div className="mt-4">
          <h5>Weather:</h5>
          <ul>
            <li>Temperature: {weather.temp} °C</li>
            <li>Humidity: {weather.humidity} %</li>
            <li>Pressure: {weather.pressure} hPa</li>
            <li>Wind Speed: {weather.wind_speed} m/s</li>
            <li>Description: {weather.description}</li>
          </ul>
          <h5>Yield Forecast:</h5>
          <ul>
            <li>3 months: {forecast.yield['3_months']}</li>
            <li>6 months: {forecast.yield['6_months']}</li>
            <li>12 months: {forecast.yield['12_months']}</li>
          </ul>
          <h5>Price Forecast:</h5>
          <ul>
            <li>3 months: {forecast.price['3_months']}</li>
            <li>6 months: {forecast.price['6_months']}</li>
            <li>12 months: {forecast.price['12_months']}</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default ForecastPage;
