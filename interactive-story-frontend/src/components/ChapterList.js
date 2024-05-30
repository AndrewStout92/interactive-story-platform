import React, { useState, useEffect } from 'react';
import api from '../api'; // Adjust the path as needed
import { useParams } from 'react-router-dom';

const ChapterList = () => {
  const { storyId } = useParams();
  const [chapters, setChapters] = useState([]);

  useEffect(() => {
    const fetchChapters = async () => {
      try {
        const data = await api.getChapters(storyId);
        setChapters(data);
      } catch (error) {
        console.error('Error fetching chapters:', error);
      }
    };

    fetchChapters();
  }, [storyId]);

  return (
    <div>
      <h1>Chapters</h1>
      <ul>
        {chapters.map((chapter) => (
          <li key={chapter.id}>{chapter.content}</li>
        ))}
      </ul>
    </div>
  );
};

export default ChapterList;