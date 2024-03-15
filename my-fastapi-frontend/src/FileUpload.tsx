import React, { useState } from 'react';
import axios from 'axios';

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [collectionName, setCollectionName] = useState<string>('');
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFile(event.target.files ? event.target.files[0] : null);
  };

  const handleCollectionNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCollectionName(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (file && collectionName) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('collection_name', collectionName);
      try {
        const response = await axios.post('http://localhost:8000/process-file', formData, {
          headers: {
            // 'Content-Type': 'multipart/form-data',
          },
        });
        setUploadStatus(response.data.message);
      } catch (error) {
        setUploadStatus('Failed to upload file.');
        console.error(error);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Collection Name:
        <input type="text" value={collectionName} onChange={handleCollectionNameChange} />
      </label>
      <label>
        Upload File:
        <input type="file" onChange={handleFileChange} />
      </label>
      <button type="submit">Upload</button>
      <div>Status: {uploadStatus}</div>
    </form>
  );
};

export default FileUpload;