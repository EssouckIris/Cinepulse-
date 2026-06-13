import MovieCard from "./MovieCard";

export default function
RecommendationList({ movies = [] }) {
    return(
<div className="
grid
grid-cols-2
md:grid-cols-4
gap-6
mt-8"
>
    {movies.map((movie, index) =>(
        <MovieCard
        key={index}
        movie={movie}
        />
    ))}
</div>
    );
}