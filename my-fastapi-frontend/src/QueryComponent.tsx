import React, { useState } from 'react';
import axios from 'axios';

const QueryComponent: React.FC = () => {
  const [collectionName, setCollectionName] = useState<string>('');
  const [query, setQuery] = useState<string>('');
  const [queryResult, setQueryResult] = useState<string>('');

  const handleCollectionNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCollectionName(event.target.value);
  };

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (collectionName && query) {
      try {
        const response = await axios.post('http://localhost:8000/query', {
          collection_name: collectionName,
          query: query,
        });
        setQueryResult(JSON.stringify(response.data));
      } catch (error) {
        setQueryResult('Failed to process query.');
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
        Query:
        <input type="text" value={query} onChange={handleQueryChange} />
      </label>
      <button type="submit">Submit Query</button>
      <div>Result: {queryResult}</div>
    </form>
  );
};

export default QueryComponent;
