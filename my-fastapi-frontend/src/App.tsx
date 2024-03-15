import React from 'react';
import logo from './logo.svg';
import './App.css';
import FileUpload from './FileUpload';
import QueryComponent from './QueryComponent';
function App() {
  return (
    <div className="App">
      <header className="RAG APP">
        <img src={logo} className="App-logo" alt="logo" />
        <FileUpload />
        <QueryComponent />
      </header>
    </div>
  );
}

export default App;
