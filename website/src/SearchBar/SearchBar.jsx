import React, { useState, useRef } from "react";
import axios from "axios";
import Keyword from "./Keyword"; // Assuming Keyword component is in a separate file


function SearchBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [keywords, setKeywords] = useState([]);
  const [maxWords, setMaxWords] = useState("");
  const [minWords, setMinWords] = useState("");
  const [langauge, setLangauge] = useState("");
  const searchInputRef = useRef(null);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/search-pog", {
        searchTerm: searchTerm,
        maxWords: maxWords,
        minWords: minWords,
        language: langauge,
      });
      console.log(response.data);
      setSearchResults(response.data);
      onSearch(searchTerm);
      setKeywords(response.data.keywords);
    } catch (error) {
      console.error("Error searching:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const keyword = event.dataTransfer.getData("text/plain");
    setSearchTerm(keyword);
    searchInputRef.current.focus();
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        ref={searchInputRef}
      />
      <button onClick={handleSearch}>Search</button>

      <label>
        Minimum Words:
        <select value={minWords} onChange={(e) => setMinWords(e.target.value)}>
          <option value="">Select</option>
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="30">30</option>
          <option value="40">40</option>
          {/* Add more options as needed */}
        </select>
      </label>

      <label>
        Maximum Words:
        <select value={maxWords} onChange={(e) => setMaxWords(e.target.value)}>
          <option value="">Select</option>
          <option value="50">50</option>
          <option value="70">70</option>
          <option value="90">90</option>
          <option value="100">100</option>
          {/* Add more options as needed */}
        </select>
      </label>

      <label>
        Select Langauge:
        <select value = {langauge} onChange={(e) => setLangauge(e.target.value)}>
        <option value="">Select</option>
        <option value="en">English</option>
        <option value="hi">hindi</option>
        </select>
      </label>

      {loading && <p>Loading...</p>}

      {searchResults && !loading && (
        <div>
          <h2><a href={searchResults.url}>Title: {searchResults.title}</a></h2>
          <p><b>Summary</b>: {searchResults.summary}</p>
          <p><strong>Keywords</strong>: {searchResults.keywords.join(", ")}</p>
          <h1>
            Interested Articles:
          </h1>
          <ul>
            {searchResults.keyWordArticles[0].map((url, index) => (
              <li key={index}>
                <a href={url}>{searchResults.keyWordArticles[1][index]}</a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default SearchBar;