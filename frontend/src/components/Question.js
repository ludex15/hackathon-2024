import React, { useState, useEffect } from 'react';

const Question = ({ onNewQuestion, onResponse }) => {
  const [inputValue, setInputValue] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  // Fetch datasets from backend
  const fetchDatasets = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/datasets');
      const data = await response.json();

      if (Array.isArray(data.files)) {
        setDatasets(data.files);
        setSelectedDataset(data.files[0] || '');
      } else {
        console.error('Unexpected response format:', data);
        setDatasets([]);
      }
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, []);

  // Handle question input change
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  // Handle dataset selection change
  const handleDatasetChange = (event) => {
    setSelectedDataset(event.target.value);
  };

  // Handle file selection for upload
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('File uploaded successfully.');
        await fetchDatasets();
      } else {
        console.error('Error uploading file:', await response.text());
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setUploading(false);
    }
  };

  // Handle form submission for a question
  const handleSubmit = async (event) => {
    event.preventDefault();
    const question = inputValue.trim();
    if (!question) return;

    onNewQuestion(question);
    setInputValue('');

    try {
      const response = await fetch('http://127.0.0.1:8000/api/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ datasetName: selectedDataset, prompt: question }),
      });

      const data = await response.json();
      if (data.content && data.content.length === 0) {
        onResponse(question, { error: 'No results found for your query.' });
      } else {
        onResponse(question, data);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="prompt">
      <div className="upload-component">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          id="files"
          style={{ display: 'none' }}
        />
        <label
        htmlFor="files"
        >
        {selectedFile ? selectedFile.name : 'Select file'}
      </label>
        <button onClick={handleFileUpload} disabled={uploading || !selectedFile}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      <form onSubmit={handleSubmit}>
        <select
          className="dataset-dropdown"
          value={selectedDataset}
          onChange={handleDatasetChange}
          disabled={datasets.length === 0}
        >
          {datasets.map((dataset) => (
            <option key={dataset} value={dataset}>
              {dataset}
            </option>
          ))}
        </select>

        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter your question"
        />
        <button type="submit" disabled={!selectedDataset}>
          Submit
        </button>
      </form>
    </div>
  );
};

export default Question;
