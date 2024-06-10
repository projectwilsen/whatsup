import { useState, useEffect } from 'react';
import './App.css';
import backgroundImage from './assets/background.svg';
import hello from './assets/hand.svg';
import Card from '/src/components/Card';

import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
const supabaseClient = createClient(supabaseUrl, supabaseKey);

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [noResults, setNoResults] = useState(false);

  useEffect(() => {
    fetchPaper();
  }, []);

  const fetchPaper = async () => {
    setIsLoading(true);
    const { data, error } = await supabaseClient
      .from('research_papers')
      .select('*')
      .order('published_date', { ascending: false })
      .limit(9);

    setIsLoading(false);

    if (error) {
      console.log(error);
    } else {
      console.log(data);
      setSearchResults(data);
      setNoResults(data.length === 0);
    }
  };

  const handleChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setNoResults(false);

    if (searchTerm.trim() === '') {
      await fetchPaper();
    } else {
      const semanticSearch = await fetch('http://127.0.0.1:8000/api/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: searchTerm,
        }),
      });

      const semanticSearchResponse = await semanticSearch.json();
      console.log(semanticSearchResponse[0][1]);
      setSearchResults(semanticSearchResponse[0][1]);
      setNoResults(semanticSearchResponse[0][1].length === 0);
    }

    setIsLoading(false);
  };

  return (
    <>
      <div className="w-full flex justify-center items-center mb-10 fixed top-0 right-0 left-0 bg-gradient-to-b from-blue-950 to-black">
        <div className="flex flex-col items-start">
          <h1 className="text-[160px] font-bold text-white mr-8 flex-shrink-0 whitespace-nowrap">What's Up!</h1>
          <form
            onSubmit={handleSubmit}
            className="bg-white rounded-lg shadow-md flex w-full px-4 py-2 mb-[50px]"
          >
            <input
              type="text"
              placeholder="Gain new insights here..."
              className="flex-grow text-lg font-light focus:outline-none"
              value={searchTerm}
              onChange={handleChange}
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-900 text-white rounded-r-lg"
            >
              Search
            </button>
          </form>
        </div>
      </div>

      <div className="flex flex-wrap justify-evenly overflow-y-auto pt-[335px]">
        {isLoading ? (
          <div className="flex justify-center items-center w-full h-full">
            <div className="loader text-white"> Loading .....</div>
          </div>
        ) : noResults ? (
          <div className="text-white text-xl mt-10">No results found</div>
        ) : (
          searchResults.map((paper, index) => (
            <Card key={index} paper={paper} />
          ))
        )}
      </div>

      <div className="text-white m-30 pt-10">
        build things with AI
      </div>
    </>
  );
}


