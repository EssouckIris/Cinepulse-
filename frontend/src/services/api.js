import axios from "axios";

const API = axios.create({
    baseURL: "https://zestful-liberation-production-0a3c.up.railway.app"
});
export const getRecommendations = (index)=>
    API.get(`/recommend/${index}`)

export const searchByTitle= (title) =>
    API.get(`/recommend_by_name?title=${encodeURIComponent(title)}`);
export default API;
