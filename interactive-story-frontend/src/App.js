import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import StoryList from './components/StoryList';
import CreateStory from './components/CreateStory';
import Register from './components/Register';
import Login from './components/Login';
import ChapterList from './components/ChapterList';
import CreateChapter from './components/CreateChapter';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/create-story" element={isAuthenticated ? <CreateStory /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/story/:storyId/chapters" element={isAuthenticated ? <ChapterList /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/story/:storyId/create-chapter" element={isAuthenticated ? <CreateChapter /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/" element={isAuthenticated ? <StoryList /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
      </Routes>
    </Router>
  );
};

export default App;




