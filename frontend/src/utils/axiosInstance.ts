import axios from "axios";

const openAIBaseURL = import.meta.env.VITE_OPEN_AI_GENERATOR_BASE_URL;

export const openAiAxiosInstance = axios.create({
  baseURL: openAIBaseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

openAiAxiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const sympyBaseURL = import.meta.env.VITE_SYMPY_GENERATOR_BASE_URL;

export const sympyAxiosInstance = axios.create({
  baseURL: sympyBaseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

sympyAxiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});