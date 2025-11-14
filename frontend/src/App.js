// frontend/src/App.js

import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import UploadPage from "./components/UploadPage";
import ForecastPage from "./components/ForecastPage";

function App() {
  return (
    <Router>
      <div style={{ padding: "20px" }}>
        <h1>AI Agriculture Platform</h1>

        <nav style={{ marginBottom: "20px" }}>
          <Link to="/upload" style={{ marginRight: "15px" }}>
            Upload Image
          </Link>

          <Link to="/forecast">
            Forecast
          </Link>
        </nav>

        <Routes>
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/forecast" element={<ForecastPage />} />
          <Route path="*" element={<h2>Select a page from above.</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
