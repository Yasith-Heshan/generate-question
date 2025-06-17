import axios from "axios";

const openAIBaseURL = import.meta.env.VITE_OPEN_AI_GENERATOR_BASE_URL;

console.log(`OpenAI Base URL: ${openAIBaseURL}`);

export const openAiAxiosInstance = axios.create({
  baseURL: openAIBaseURL,
  headers: {
    "Content-Type": "application/json",
  },
});
