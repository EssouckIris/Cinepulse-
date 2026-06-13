import axios from "axios";

const API = axios.create({
    baseURL: "https://cinepulse-production-3830.up.railway.app"
});
export const getRecommendations = (index)=>
    API.get(`/recommend/${index}`)

export const searchByTitle= (title) =>
    API.get(`/recommend_by_name?title=${encodeURIComponent(title)}`);
export default API;
