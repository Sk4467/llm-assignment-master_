// // QueryComponent.tsx
import React, { useState } from 'react';
import axios from 'axios';
import './QueryComponent.css'; // Import CSS file

const QueryComponent: React.FC = () => {
  const [collectionName, setCollectionName] = useState<string>('');
  const [query, setQuery] = useState<string>('');
  const [queryResult, setQueryResult] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const handleCollectionNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCollectionName(event.target.value);
  };

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/query', {
        collection_name: collectionName,
        query: query,
      });
      setQueryResult(JSON.stringify(response.data.result));
    } catch (error: any) {
      setQueryResult('Failed to process query.');
    }
  };

  return (
    <div className="query-container">
      <form onSubmit={handleSubmit}>
        <label>
          Collection Name:
          <input type="text" value={collectionName} onChange={handleCollectionNameChange} />
        </label>
        <br />
        <label>
          Query:
          <input type="text" value={query} onChange={handleQueryChange} />
        </label>
        <br />
        <button type="submit">Submit Query</button>
      </form>
      <textarea
        className="query-result"
        value={queryResult}
        readOnly // Makes the textarea not editable
      />
    </div>
  );
};

export default QueryComponent;