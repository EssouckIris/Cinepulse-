import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:5000"
});
export const getRecommendations = (index)=>
    API.get(`/recommend/${index}`)

export const searchByTitle= (title) =>
    API.get(`/recommend_by_name?title=${encodeURIComponent(title)}`);
export default API;
