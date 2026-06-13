import { useState, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import RecommendationList from "../components/Recommendation";
import Navbar from "../components/Navbar";
import { getRecommendations, searchByTitle } from "../services/api";

export default function Home() {
  const [movies, setMovies] = useState([]);

  const format = (data) =>
  data.map((movie) => ({
    title: movie.title,
    poster: movie.poster,
    genre: movie.genre,
    rating: "N/A",
  }));

  useEffect(() => {
    getRecommendations(0)
      .then((res) => setMovies(format(res.data.recommended_movies)))
      .catch((err) => console.log(err));
  }, []);

  
const handleSearch = (movieName) => {
  searchByTitle(movieName)
    .then((res) => setMovies(format(res.data.recommended_movies)))
    .catch((err) => console.log(err));
};
  return (
    <div className="min-h-screen bg-black">
      <Navbar />
      <div className="flex flex-col items-center px-4 pb-10 pt-10">
        <p className="text-gray-400 text-sm mt-2">
          Trouve des films similaires à tes favoris
        </p>
        <SearchBar onSearch={handleSearch} />
        <RecommendationList movies={movies} />
      </div>
    </div>
  );
}