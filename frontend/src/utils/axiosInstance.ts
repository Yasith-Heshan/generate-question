import axios from "axios";

const openAIBaseURL = import.meta.env.VITE_OPEN_AI_GENERATOR_BASE_URL;

export const openAiAxiosInstance = axios.create({
  baseURL: openAIBaseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

const sympyBaseURL = import.meta.env.VITE_SYMPY_GENERATOR_BASE_URL;

export const sympyAxiosInstance = axios.create({
  baseURL: sympyBaseURL,
  headers: {
    "Content-Type": "application/json",
  },
});