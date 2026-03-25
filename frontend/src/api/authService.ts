import { openAiAxiosInstance as axios } from "../utils/axiosInstance";
import type { UserCreateRequest, UserLoginRequest } from "../utils/interface";

export const signup = async (user: UserCreateRequest) => {
  return await axios.post("/api/v1/auth/signup", user);
};

export const login = async (user: UserLoginRequest) => {
  return await axios.post("/api/v1/auth/login", user);
};

export const getProfile = async () => {
  return await axios.get("/api/v1/auth/me");
};
