import React, { useState, useEffect } from 'react';

const UploadComponent = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    setUploading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        onUploadSuccess(data.files);
      } else {
        console.error('Error uploading file:', response.statusText);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-component">
      <input type="file" onChange={handleFileChange} accept=".csv" />
      <button onClick={handleUpload} disabled={uploading || !selectedFile}>
        {uploading ? 'Uploading...' : 'Upload CSV'}
      </button>
    </div>
  );
};

export default UploadComponent;