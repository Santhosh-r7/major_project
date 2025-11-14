// frontend/src/components/UploadPage.jsx
import React, { useState } from 'react';
import axios from 'axios';

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [severity, setSeverity] = useState(null);
  const [recommendation, setRecommendation] = useState('');
  const [overlayUrl, setOverlayUrl] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append('image', selectedFile);  // send file as 'image'
    axios.post('/api/segment', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then(res => {
      setSeverity(res.data.severity.toFixed(2));
      setRecommendation(res.data.recommendation);
      setOverlayUrl(res.data.overlay);
    })
    .catch(err => {
      console.error(err);
      alert('Error processing image');
    });
  };

  return (
    <div>
      <h3>Upload Crop Image for Segmentation</h3>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button className="btn btn-success mx-2" onClick={handleUpload}>Segment</button>
      {severity !== null && (
        <div className="mt-4">
          <h5>Disease Severity: {severity}%</h5>
          <p><strong>Recommendation:</strong> {recommendation}</p>
          <img src={overlayUrl} alt="Overlay" style={{maxWidth: '400px'}} />
        </div>
      )}
    </div>
  );
}

export default UploadPage;
