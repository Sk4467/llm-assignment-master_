// import React, { useState } from 'react';
// import axios from 'axios';

// const FileUpload: React.FC = () => {
//   const [file, setFile] = useState<File | null>(null);
//   const [collectionName, setCollectionName] = useState<string>('');
//   const [uploadStatus, setUploadStatus] = useState<string>('');

//   const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//     setFile(event.target.files ? event.target.files[0] : null);
//   };

//   const handleCollectionNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//     setCollectionName(event.target.value);
//   };

//   const handleSubmit = async (event: React.FormEvent) => {
//     event.preventDefault();
//     if (file && collectionName) {
//       const formData = new FormData();
//       formData.append('file', file);
//       formData.append('collection_name', collectionName);
//       try {
//         const response = await axios.post('http://localhost:8000/process-file', formData, {
//           headers: {
//             // 'Content-Type': 'multipart/form-data',
//           },
//         });
//         setUploadStatus(response.data.message);
//       } catch (error:any) {
//         setUploadStatus(error.response?.data?.detail || 'Failed to upload file.');
//       }
//     }else {
//       setUploadStatus('Please select a file and enter a collection name.');
//     }
//   };

//   return (
//     <div>
//       <form onSubmit={handleSubmit}>
//         <label>
//           Collection Name:
//           <input type="text" value={collectionName} onChange={handleCollectionNameChange} />
//         </label>
//         <br />
//         <label>
//           Upload File (PDF, DOCX, CSV, TXT only):
//           <input type="file" onChange={handleFileChange} accept=".pdf,.docx,.csv,.txt" />
//         </label>
//         <br />
//         <button type="submit">Upload</button>
//       </form>
//       <div>Status: {uploadStatus}</div>
//     </div>
//   );
// };

// export default FileUpload;
// FileUpload.tsx
import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css'; // Import CSS file

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [collectionName, setCollectionName] = useState<string>('');
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [showNotification, setShowNotification] = useState<boolean>(false);
  // const [isLoading, setIsLoading] = useState(false);
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
        const response = await axios.post('http://localhost:8000/process-file', formData);
        setUploadStatus(response.data.message);
        setShowNotification(true);
        setTimeout(() => setShowNotification(false), 3000); // Hide notification after 3 seconds
      } catch (error: any) {
        setUploadStatus(error.response?.data?.detail || 'Failed to upload file.');
      }
    }
  };

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit}>
        <label>
          Collection Name:
          <input type="text" value={collectionName} onChange={handleCollectionNameChange} />
        </label>
        <br />
        <label>
          Upload File (PDF, DOCX, CSV, TXT only):
          <input type="file" onChange={handleFileChange} accept=".pdf,.docx,.csv,.txt" />
        </label>
        <br />
        <button type="submit">Upload</button>
      </form>
      {showNotification && (
        <div className="notification-popup">File uploaded successfully!</div>
      )}
    </div>
  );
};

export default FileUpload;