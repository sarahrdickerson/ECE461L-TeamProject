import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  useEffect(() => {
    fetch('/login').then(response => {
      return response.text();
    }).then(html => {
      document.body.innerHTML = html;
    });
  }, []);
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>welcome to the landing page! </h1>
        <img src={require(".//assets/logo_white.png")} className="App-logo" alt="logo" />
        <p>
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
        </a>
        
      </header>
    </div>
  );
}

export default App;
