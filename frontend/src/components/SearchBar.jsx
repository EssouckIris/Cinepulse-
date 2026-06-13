import { useState } from "react";

export default function SearchBar({
    onSearch
}){
const [movieName, setMovieName] = useState("");

const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(movieName)
};
return(
    <form
    onSubmit={handleSubmit}
    className="
    flex
    gap-4
    mt-6
    "
    >
        <input
        type="text"
        placeholder="Search a movie..."
        value={movieName}
        onChange={(e)=>
            setMovieName(e.target.value)
        }
        className="
        flex-1
        p-3
        rounded-lg
        bg-[#111]
        text-white
        border
        border-fuchsiaTheme
        outline-none
        "
        />

        <button

        type="submit"

        className="
        bg-fuchsiaTheme
        text-back
        px-6
        py-3
        rounded-lg
        font-bold
        hover:scale-105
        Transition
        "
        >
        Search
        </button>
    </form>
);
}