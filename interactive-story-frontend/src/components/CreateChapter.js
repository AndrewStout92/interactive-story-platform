import React, { useState } from 'react';
import api from '../api'; // Adjust the path as needed
import { useParams } from 'react-router-dom';

const CreateChapter = () => {
  const { storyId } = useParams();
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createChapter({ story_id: storyId, content });
      setContent('');
      // Add any additional handling or redirects as needed
    } catch (error) {
      console.error('Error creating chapter:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Content:
        <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
      </label>
      <button type="submit">Create Chapter</button>
    </form>
  );
};

export default CreateChapter;