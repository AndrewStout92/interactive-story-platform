import React, { useState } from 'react';
import api from '../api'; // Adjust the path as needed

const CreateStory = () => {
  const [title, setTitle] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createStory({ title });
      setTitle('');
      // Add any additional handling or redirects as needed
    } catch (error) {
      console.error('Error creating story:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Title:
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
      </label>
      <button type="submit">Create Story</button>
    </form>
  );
};

export default CreateStory;

