import React from 'react';
import { AppProvider } from './context/AppContext';
import App from './App';

export default function VocabAgent() {
  return (
    <AppProvider>
      <App />
    </AppProvider>
  );
}
